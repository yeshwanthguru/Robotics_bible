import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './index.module.css';

const MAIN = [
  {title: 'Handbook', desc: 'Plain-English chapters with diagrams and technical depth: ML to robotics to simulation.', to: '/docs/'},
  {title: 'Dictionary A–Z', desc: 'Over 1,000 terms, each with a one-line definition and a link to the chapter.', to: '/docs/glossary'},
  {title: 'Interview Q&A', desc: 'Hundreds of questions with short answers and deeper follow-ups, by domain.', to: '/docs/interview/question-bank'},
  {title: 'Build It Yourself', desc: 'Step-by-step guides with tested code: AI model, VLM and VLA.', to: '/docs/build-your-own/start-building'},
  {title: 'Reference', desc: 'Tools, datasets, landmark papers and robot platforms directories.', to: '/docs/reference/tools-libraries'},
  {title: 'Cheat Sheets', desc: 'Formulas in words, commands and glossary on one page each.', to: '/docs/cheatsheets/formulas'},
];

const DOMAINS = [
  ['Machine learning', '/docs/machine-learning/ml-fundamentals'],
  ['Deep learning', '/docs/deep-learning/dl-fundamentals'],
  ['Reinforcement learning', '/docs/reinforcement-learning/rl-foundations'],
  ['LLM', '/docs/foundation-models/llm'],
  ['VLM and VLA', '/docs/foundation-models/vlm-vla'],
  ['Quantum computing', '/docs/quantum/quantum-basics'],
  ['Physical AI', '/docs/physical-ai/physical-ai-overview'],
  ['Kinematics', '/docs/robotics/kinematics'],
  ['Dynamics', '/docs/robotics/dynamics'],
  ['Control', '/docs/planning-control/control'],
  ['Motion planning', '/docs/planning-control/motion-planning'],
  ['SLAM and localization', '/docs/perception-localization/slam-localization'],
  ['Perception', '/docs/perception-localization/computer-vision-3d'],
  ['Mobility', '/docs/mobility-dexterity/mobile-navigation'],
  ['Legged locomotion', '/docs/mobility-dexterity/legged-locomotion'],
  ['Manipulation and dexterity', '/docs/mobility-dexterity/manipulation-dexterity'],
  ['ROS 2', '/docs/software/ros2'],
  ['C++ and Python', '/docs/software/cpp-for-robotics'],
  ['MATLAB, R, PDDL', '/docs/software/matlab-simulink'],
  ['Isaac Sim', '/docs/simulation/isaac-sim'],
  ['Isaac Lab', '/docs/simulation/isaac-lab'],
  ['Isaac Gym', '/docs/simulation/isaac-gym'],
  ['Sim-to-real', '/docs/simulation/sim2real'],
  ['Safety and ethics', '/docs/robotics/safety-ethics-standards'],
];

export default function Home() {
  return (
    <Layout title="Robotics & AI Bible" description="A lifelong handbook, dictionary and Q&A for AI and robotics">
      <header className={styles.hero}>
        <div className="container">
          <h1 className={styles.title}>Robotics &amp; AI Bible</h1>
          <p className={styles.tagline}>
            One searchable handbook, dictionary and interview Q&amp;A for machine learning, deep learning, reinforcement
            learning, LLM / VLM / VLA, quantum computing, Physical AI, robotics and simulation.
          </p>
          <p className={styles.hint}>
            Press <kbd>Ctrl</kbd> + <kbd>K</kbd> and type any word: <em>Kalman</em>, <em>PPO</em>, <em>QoS</em>, <em>Isaac Lab</em>…
          </p>
          <div className={styles.buttons}>
            <Link className="button button--primary button--lg" to={'/docs/'}>Open the handbook</Link>
            <Link className="button button--secondary button--lg" to={'/docs/glossary'}>Dictionary A–Z</Link>
          </div>
        </div>
      </header>
      <main className="container">
        <section className={styles.grid}>
          {MAIN.map((c) => (
            <Link key={c.title} to={c.to} className={styles.card}>
              <h3>{c.title}</h3>
              <p>{c.desc}</p>
            </Link>
          ))}
        </section>
        <h2 className={styles.h2}>Jump to a topic</h2>
        <section className={styles.chips}>
          {DOMAINS.map(([name, to]) => (
            <Link key={name} to={to} className={styles.chip}>{name}</Link>
          ))}
        </section>
      </main>
    </Layout>
  );
}
