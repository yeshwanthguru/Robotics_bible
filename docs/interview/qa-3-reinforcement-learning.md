---
title: "Q&A 3: Reinforcement Learning"
---

# Interview Q&A: Reinforcement Learning

:::tip[How to use]
Chapters: [RL foundations](../04-reinforcement-learning/rl-foundations.md) · [Imitation & robot learning](../07-physical-ai/imitation-robot-learning.md).
:::

## Foundations

### Q: Define an MDP.
**Short answer:** States, actions, transition probabilities, rewards and a discount factor, with the Markov property. **Go deeper:** If the agent only sees part of the state it is a POMDP and needs memory or a belief.

### Q: What is the Bellman equation?
**Short answer:** The value of a state is the reward now plus the discounted value of what comes next. **Go deeper:** The optimality version uses a max over actions; its fixed point is the optimal value function (a contraction for γ < 1).

### Q: Value function versus Q-function versus advantage?
**Short answer:** V is how good a state is; Q is how good an action is in a state; advantage is Q − V. **Go deeper:** Subtracting V as a baseline reduces gradient variance without bias.

### Q: What does the discount factor do?
**Short answer:** It weights near-term rewards more than distant ones. **Go deeper:** γ close to 1 gives long-sighted behaviour but harder learning; it also keeps infinite sums finite.

### Q: On-policy versus off-policy?
**Short answer:** On-policy learns from fresh data of the current policy; off-policy can reuse old data. **Go deeper:** PPO is on-policy and stable but sample-hungry; SAC is off-policy and sample-efficient.

### Q: Model-free versus model-based RL?
**Short answer:** Model-free learns a policy or value directly; model-based learns a dynamics model and plans with it. **Go deeper:** Model-based is more sample-efficient but suffers from model bias; Dreamer and TD-MPC2 address this.

### Q: What is exploration versus exploitation?
**Short answer:** Trying new things to learn versus using what works. **Go deeper:** ε-greedy, entropy bonuses, UCB, Thompson sampling, curiosity bonuses.

### Q: What is the deadly triad?
**Short answer:** Function approximation, bootstrapping and off-policy data together can diverge. **Go deeper:** Target networks, replay and conservative updates mitigate it.

### Q: Why does DQN overestimate values and how is it fixed?
**Short answer:** The max over noisy estimates is biased upward. **Go deeper:** Double DQN picks the action with one network and evaluates it with another.

## Policy gradient and actor–critic

### Q: Explain the policy gradient theorem.
**Short answer:** Increase the probability of actions in proportion to how good they turned out. **Go deeper:** ∇J = E[∇log π(a|s) · A]; baselines reduce variance.

### Q: What is GAE?
**Short answer:** Generalised advantage estimation blends multi-step returns. **Go deeper:** λ trades bias (small λ) against variance (large λ).

### Q: Explain PPO and its clip.
**Short answer:** It improves the policy while clipping how much the action probabilities can change per update. **Go deeper:** Objective min(rA, clip(r, 1±ε)A) is a cheap stand-in for a trust region; it also uses a value loss and entropy bonus.

### Q: Why is PPO the default for locomotion in Isaac Lab?
**Short answer:** It is stable, simple and scales with thousands of parallel simulated robots. **Go deeper:** Large batches reduce its sample inefficiency.

### Q: SAC versus PPO versus TD3?
**Short answer:** SAC maximises reward plus entropy off-policy; PPO is on-policy clipped; TD3 is a deterministic off-policy actor-critic with twin critics. **Go deeper:** Use SAC when real data is expensive, PPO when simulation is cheap and parallel.

### Q: What is entropy regularisation for?
**Short answer:** It keeps the policy random enough to explore and avoid collapsing too early. **Go deeper:** SAC auto-tunes the temperature α to hit a target entropy.

### Q: Why use a replay buffer and target network?
**Short answer:** Replay breaks correlation between samples; target networks stabilise bootstrapped targets. **Go deeper:** Prioritised replay samples surprising transitions more.

### Q: How do you handle continuous actions?
**Short answer:** Use a Gaussian policy (PPO/SAC) or a deterministic actor (DDPG/TD3). **Go deeper:** Squash outputs with tanh and scale to action limits; DQN needs discrete actions.

## Practice

### Q: How do you design a reward function?
**Short answer:** Start with a clear success signal, add dense shaping terms, and check behaviour by watching videos. **Go deeper:** Weight terms carefully (tracking, energy, smoothness, termination), use potential-based shaping to keep the optimum, and watch for reward hacking.

### Q: What is reward hacking? Give an example.
**Short answer:** The agent exploits a loophole to score high without doing the task. **Go deeper:** E.g. a robot vibrating to collect an "alive" bonus; fix the reward or add constraints.

### Q: How do you deal with sparse rewards?
**Short answer:** Shape the reward, use curricula, demonstrations, or hindsight relabelling. **Go deeper:** HER turns failures into successes for other goals; curiosity bonuses help exploration.

### Q: How do you treat time-outs versus true terminations?
**Short answer:** A time-out should still bootstrap the value; a failure should not. **Go deeper:** Mixing them up biases value estimates and is a classic bug.

### Q: How do you debug RL?
**Short answer:** Check reward scale, observation normalisation, termination handling and seeds, test on a trivial environment, and watch videos. **Go deeper:** Log entropy, KL, value explained variance and gradient norms.

### Q: Why normalise observations and advantages?
**Short answer:** It keeps learning stable across scales. **Go deeper:** Running mean/std for observations, per-batch normalisation of advantages.

### Q: What is curriculum learning?
**Short answer:** Train on easy tasks first and gradually increase difficulty. **Go deeper:** E.g. terrain difficulty in legged locomotion increases with success.

### Q: What is asymmetric actor–critic?
**Short answer:** The critic sees privileged simulator data; the actor sees only deployable observations. **Go deeper:** It improves value estimates without leaking unavailable info into the deployed policy.

### Q: How do you make an RL policy transfer to hardware?
**Short answer:** Randomise physics and sensing, model the actuators and delays, regularise action smoothness, and test sim-to-sim first. **Go deeper:** See the sim-to-real chapter.

## Offline RL, imitation and beyond

### Q: What is the main problem of offline RL?
**Short answer:** The policy may pick actions not in the dataset whose values are over-estimated. **Go deeper:** CQL penalises such Q-values; IQL avoids out-of-distribution queries; TD3+BC regularises toward the data.

### Q: Behavior cloning versus DAgger?
**Short answer:** BC trains on expert states only; DAgger also trains on states the learner visits, with expert labels. **Go deeper:** BC error grows like T²ε; DAgger like Tε.

### Q: What is GAIL?
**Short answer:** A discriminator tells expert from learner trajectories and its output becomes the learner's reward. **Go deeper:** It avoids hand-written rewards but needs on-policy RL in the loop.

### Q: What is inverse RL?
**Short answer:** Infer the reward the expert must have been optimising. **Go deeper:** Max-entropy IRL resolves ambiguity by preferring the least committal distribution over behaviours.

### Q: What is RLHF and how is DPO different?
**Short answer:** RLHF trains a reward model from preferences and optimises against it with RL; DPO optimises directly on preference pairs with a simple loss. **Go deeper:** DPO is offline and simpler; RLHF can explore online.

### Q: What is GRPO?
**Short answer:** A policy-gradient method that scores a group of sampled answers relative to each other, with no value network. **Go deeper:** Popular for reasoning models with verifiable rewards.

### Q: What is hierarchical RL?
**Short answer:** A high-level policy sets goals or picks skills and low-level policies execute them. **Go deeper:** Options, feudal networks, skill discovery (DIAYN).

### Q: What is safe RL?
**Short answer:** Learning under constraints on risk. **Go deeper:** Constrained MDPs, Lagrangian methods, CPO, shielding and CBF safety filters.

### Q: What is a world model in RL?
**Short answer:** A learned predictor of next states used to plan or to train in imagination. **Go deeper:** Dreamer learns a latent model and optimises the policy on imagined rollouts.

### Q: When would you choose RL over imitation learning?
**Short answer:** When you cannot demonstrate the behaviour, simulation is cheap, and the reward is clear. **Go deeper:** Locomotion and fast in-hand manipulation are typical; manipulation with language often uses imitation first.

### Q: What is residual RL?
**Short answer:** Learn a small correction on top of a hand-designed or imitation base controller. **Go deeper:** It keeps the base's safety and speeds learning.

### Q: What is multi-agent RL's central difficulty?
**Short answer:** From each agent's view the environment is non-stationary because others also learn. **Go deeper:** Centralised training with decentralised execution (MAPPO, QMIX) is the common fix.
