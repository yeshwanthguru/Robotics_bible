---
title: C++ for Robotics
---

# C++ (C++17/20) for Robotics

## Language essentials interviewers probe
- **RAII & ownership:** `std::unique_ptr` (sole), `std::shared_ptr` (ref-count; `weak_ptr` breaks cycles), prefer `make_unique/make_shared`; rule of 0/3/5.
- **Move semantics:** rvalue refs, `std::move`, `std::forward` (perfect forwarding), copy elision (guaranteed in C++17).
- **Templates & concepts:** SFINAE vs C++20 `concepts`, variadic templates, CRTP, `constexpr`/`consteval`, `if constexpr`.
- **STL:** `vector` (contiguous; `reserve` to avoid realloc), `array`, `deque`, `list`, `unordered_map`, `map`, `priority_queue`, `string_view`, `span`, `optional/variant`, `algorithm`, ranges (C++20).
- **Concurrency:** `std::thread/jthread`, `mutex`, `lock_guard/scoped_lock`, `condition_variable`, `atomic` + memory orders, `future/promise/async`, lock-free SPSC ring buffer, `shared_mutex`.
- **Virtual functions:** vtable, `override/final`, virtual destructor, slicing, pure virtual interfaces for hardware abstraction.
- **Undefined behaviour:** dangling refs, use-after-move, signed overflow, data races, uninitialized read, strict aliasing.
- **Const-correctness**, `noexcept`, `[[nodiscard]]`, `explicit`, `= delete`.

## Real-time-safe C++
No `new/delete`/`std::vector::push_back` growth, no exceptions in RT path (or use `noexcept`), no blocking syscalls/locks (use try-lock / lock-free), pre-allocated memory pools (`std::pmr`), `mlockall`, thread affinity + `SCHED_FIFO`, avoid `std::cout`, bound loops. Tools: `valgrind`, ASan/UBSan/TSan, `perf`, `gdb`, `clang-tidy`, `cppcheck`, `heaptrack`.

## Linear algebra & robotics libs
**Eigen** (`Matrix3d`, `Quaterniond`, `Isometry3d`, `.noalias()`, alignment issues `EIGEN_MAKE_ALIGNED_OPERATOR_NEW`), **Sophus/manif** (Lie groups), **GTSAM**, **Ceres**, **g2o**, **PCL**, **OpenCV**, **Pinocchio**, **KDL**, **Drake**, **OMPL**, **FCL**, **CasADi**, **OSQP**, **qpOASES**, **IPOPT**, **Boost**, **fmt/spdlog**, **yaml-cpp**, **nlohmann/json**, **gRPC/protobuf**, **Google Test/benchmark**.

## Example: pose composition with Eigen
```cpp
#include <Eigen/Geometry>
Eigen::Isometry3d T_wb = Eigen::Isometry3d::Identity();
T_wb.rotate(Eigen::AngleAxisd(M_PI/4, Eigen::Vector3d::UnitZ()));
T_wb.pretranslate(Eigen::Vector3d(1, 2, 0));
Eigen::Vector3d p_b(0.5, 0, 0);
Eigen::Vector3d p_w = T_wb * p_b;          // body → world
Eigen::Quaterniond q(T_wb.rotation());     // normalize after integrating!
```

## Example: thread-safe queue
```cpp
template <class T> class SafeQueue {
  std::queue<T> q_; mutable std::mutex m_; std::condition_variable cv_;
public:
  void push(T v) { { std::lock_guard l(m_); q_.push(std::move(v)); } cv_.notify_one(); }
  T pop() { std::unique_lock l(m_); cv_.wait(l, [&]{ return !q_.empty(); });
            T v = std::move(q_.front()); q_.pop(); return v; }
};
```

## Example: lock-free SPSC ring buffer (sketch)
```cpp
template <class T, size_t N> class Spsc {
  std::array<T, N> buf_; std::atomic<size_t> h_{0}, t_{0};
public:
  bool push(const T& v) { auto t = t_.load(std::memory_order_relaxed), n = (t+1)%N;
    if (n == h_.load(std::memory_order_acquire)) return false;
    buf_[t] = v; t_.store(n, std::memory_order_release); return true; }
  bool pop(T& v) { auto h = h_.load(std::memory_order_relaxed);
    if (h == t_.load(std::memory_order_acquire)) return false;
    v = buf_[h]; h_.store((h+1)%N, std::memory_order_release); return true; }
};
```

## CMake essentials
```cmake
cmake_minimum_required(VERSION 3.16)
project(my_robot LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
find_package(Eigen3 REQUIRED)
add_library(core src/core.cpp)
target_include_directories(core PUBLIC include)
target_link_libraries(core PUBLIC Eigen3::Eigen)
add_executable(app src/main.cpp)
target_link_libraries(app PRIVATE core)
```
Know: targets & PUBLIC/PRIVATE/INTERFACE, `find_package`, `install`, `ament_cmake` macros, cross-compiling for Jetson (toolchain file), ccache, Ninja, Conan/vcpkg.

## CUDA / GPU
Kernels, grid/block/thread, shared memory, coalesced access, streams, Thrust, cuBLAS, TensorRT C++ API, Warp (Python kernels), zero-copy with Jetson unified memory, NITROS type adaptation.

## Interview Q&A

**`shared_ptr` cost?** Atomic ref-count, control block alloc, indirection; avoid in hot paths/pass by `const&`.

**`vector<bool>`?** Bit-packed specialization, proxy reference → not a real container.

**Why `virtual ~Base()`?** Deleting derived via base pointer without it is UB.

**Stack vs heap allocation in RT?** Heap non-deterministic; use stack/pool.

**`std::move` actually moves?** No, it casts to rvalue; move ctor performs move.

**Data race vs race condition?** Data race = unsynchronized conflicting access (UB); race condition = outcome depends on timing.

**Memory order acquire/release?** Release store publishes prior writes; acquire load observes them.
