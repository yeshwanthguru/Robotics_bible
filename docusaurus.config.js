// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// Change url/baseUrl/organizationName/projectName to match the repo this lives in.
/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Robotics & AI Bible',
  tagline: 'ML · DL · RL · LLM/VLM/VLA · Quantum · Physical AI · Robotics · Simulation — one interview reference',
  favicon: 'img/favicon.svg',
  url: 'https://yeshwanthguru.github.io',
  baseUrl: '/Robotics_bible/',
  organizationName: 'yeshwanthguru',
  projectName: 'Robotics_bible',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  markdown: {mermaid: true, format: 'detect'},
  themes: [
    '@docusaurus/theme-mermaid',
    [require.resolve('@easyops-cn/docusaurus-search-local'), {hashed: true, docsRouteBasePath: '/docs', indexBlog: false}],
  ],
  stylesheets: [
    {href: 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css', type: 'text/css'},
  ],
  presets: [
    ['classic', {
      docs: {
        routeBasePath: 'docs',
        sidebarPath: './sidebars.js',
        remarkPlugins: [remarkMath],
        rehypePlugins: [rehypeKatex],
      },
      blog: false,
      theme: {customCss: './src/css/custom.css'},
    }],
  ],
  themeConfig: {
    colorMode: {defaultMode: 'dark', respectPrefersColorScheme: true},
    navbar: {
      title: 'Robotics & AI Bible',
      items: [
        {type: 'docSidebar', sidebarId: 'bible', position: 'left', label: 'Docs'},
        {to: '/docs/interview/question-bank', label: 'Interview', position: 'left'},
        {to: '/docs/cheatsheets/formulas', label: 'Cheat Sheets', position: 'left'},
      ],
    },
    footer: {style: 'dark', copyright: 'Personal interview reference. Built with Docusaurus.'},
    docs: {sidebar: {hideable: true, autoCollapseCategories: true}},
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'python', 'cpp', 'matlab', 'r', 'yaml', 'lisp', 'cmake', 'json'],
    },
  },
};
export default config;
