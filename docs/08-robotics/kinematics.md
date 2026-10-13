---
title: Spatial Math & Kinematics
---

# Spatial Math & Kinematics

:::tip[The 30-second version]
**Kinematics** = the *geometry* of motion, ignoring forces. Two questions:
**Forward kinematics (FK):** "I know the joint angles, where is the hand?" (easy, one answer).
**Inverse kinematics (IK):** "I want the hand *there*, what joint angles do I need?" (harder: zero, one, or many answers).
Everything rests on one tool: describing *where something is and how it's rotated* relative to something else.
:::

## 🎮 Try it yourself

<div class="simbox"><div class="simhead"><span>Interactive: Forward and inverse kinematics</span><a href="/Robotics_bible/sim/ik-2link.html" target="_blank">open full screen ↗</a></div><iframe src="/Robotics_bible/sim/ik-2link.html" height="560" loading="lazy" title="Forward and inverse kinematics"></iframe></div>


## Frames: every part has its own coordinate system

![frames chain](/img/fig/frames-chain.svg)
*To find the object in the world, multiply the transforms along the chain. ROS stores exactly this as the TF tree.*

A **pose** is *position + orientation* of one frame relative to another. Position is easy (three numbers). Orientation is the tricky part.

### Ways to represent orientation

| Representation | Plain idea | Pros | Cons |
|---|---|---|---|
| **Rotation matrix** (3×3) | three perpendicular arrows | easy to compose | 9 numbers for 3 degrees of freedom |
| **Euler angles** (roll-pitch-yaw) | three turns in order | intuitive | **gimbal lock**, order ambiguity |
| **Axis-angle** | spin by θ about an axis | compact | singular near 180° |
| **Quaternion** $(w,x,y,z)$ | 4 numbers with unit length | no gimbal lock, smooth interpolation | double cover ($q$ and $-q$ are the same rotation) |
| **6-D representation** | two columns of the matrix | best for neural-network outputs | needs re-orthogonalising |

> **Gimbal lock in a sentence:** when two rotation axes line up, you lose a degree of freedom, like pointing a camera straight up on a three-ring gimbal.
>
> ⚠️ **Classic bug:** ROS and SciPy store quaternions as `(x, y, z, w)`; Eigen's constructor takes `(w, x, y, z)`; MATLAB uses `[w x y z]`.

### Homogeneous transforms
Pack rotation $R$ and position $p$ into one 4×4 matrix so chaining poses is just multiplication.

$$ T=\begin{pmatrix}R&p\\0&1\end{pmatrix},\qquad T^{-1}=\begin{pmatrix}R^\top&-R^\top p\\0&1\end{pmatrix} $$

> **In words:** "to go from the hand frame to the world frame, rotate then shift. To go backwards, undo the shift then un-rotate."

Advanced but asked: **Lie groups** SO(3)/SE(3) with *exp/log maps* let you treat small rotations as vectors, the basis of modern optimisation on poses (GTSAM, Sophus). **Hand–eye calibration** solves $AX=XB$ to find where the camera sits relative to the arm.

## Forward kinematics

![two link arm](/img/fig/two-link-arm.svg)
*Left: joint angles in, hand position out; the blue disc is every place the hand can reach. Right: inverse kinematics often has two valid answers ("elbow up" and "elbow down").*

For a 2-link planar arm:
$$ x=l_1\cos q_1+l_2\cos(q_1+q_2),\qquad y=l_1\sin q_1+l_2\sin(q_1+q_2) $$

> **In words:** "walk along link 1, then along link 2, each pointing at the sum of the angles so far."

For real robots we describe the chain with **DH parameters** (4 numbers per joint) or the cleaner **product of exponentials**, and robot files (**URDF**) list links, joints, masses and meshes.

## The Jacobian: how joint speeds become hand speeds

$$ \dot x = J(q)\,\dot q,\qquad \tau = J^\top F $$

> **In words:** the Jacobian is a *local gear ratio*. It converts joint speeds into hand speed, and (transposed) hand force into joint torques.

- **Singularity:** the Jacobian loses rank, so the hand cannot move in some direction no matter what, and the inverse needs *infinite* joint speed. Typical: arm fully stretched out.
- **Manipulability:** how "easily" the hand can move in each direction (the ellipsoid from the Jacobian's SVD).
- **Redundant arms** (7 joints for a 6-D task) have spare freedom: the *null space* can avoid joint limits or obstacles without moving the hand.

## Inverse kinematics

| Method | Plain idea | Notes |
|---|---|---|
| **Analytic** | closed-form formula | fast, all solutions (IKFast) |
| **Jacobian pseudo-inverse** | repeatedly step toward the target | simple |
| **Damped least squares (LM)** | pseudo-inverse with a safety damper | **robust near singularities** |
| **Optimisation-based (QP)** | IK as constrained optimisation | joint limits, collisions (TRAC-IK, Pink, cuRobo) |
| **Learned IK** | network proposes solutions | can return several answers |

$$ \Delta q = J^\top\big(JJ^\top+\lambda^2 I\big)^{-1}\Delta x $$

> **In words:** "move the joints in the direction that helps most, but add a damping term so you don't go crazy near a singularity."

## Mobile-robot kinematics
- **Differential drive** (two wheels): forward speed = average of wheel speeds; turn rate = difference ÷ width. Cannot slide sideways ("non-holonomic").
- **Car-like (Ackermann / bicycle model):** turn rate = $v\tan\delta / L$.
- **Omni / mecanum / swerve:** can move in any direction (holonomic).

## Interview Q&A

**Why quaternions instead of Euler angles?**
*Simply:* no gimbal lock, smooth interpolation, compact and numerically safe (just renormalise).

**What is a singularity and how do you handle it?**
*Simply:* a pose where the arm loses a direction of motion. Use damped least squares, plan around it, or use null-space motion.

**Is FK or IK harder?**
*Simply:* IK. FK has exactly one answer; IK may have none, one or several, so it is solved with formulas or numerical iteration.

**Why does $\tau=J^\top F$ hold?**
*Simply:* energy balance (virtual work): joint work equals hand work.

**Why a 6-D rotation representation for neural nets?**
*Simply:* 3-D and 4-D representations have jumps that are hard to regress; the 6-D one is continuous.
