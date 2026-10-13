// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// Change url/baseUrl/organizationName/projectName to match the repo this lives in.
/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Robotics & AI Bible',
  tagline: 'A lifelong handbook, dictionary and Q&A for ML · DL · RL · LLM/VLM/VLA · Quantum · Physical AI · Robotics · Simulation',
  favicon: 'img/favicon.svg',
  url: 'https://yeshwanthguru.github.io',
  baseUrl: '/Robotics_bible/',
  organizationName: 'yeshwanthguru',
  projectName: 'Robotics_bible',
  onBrokenLinks: 'warn',
  markdown: {mermaid: true, format: 'detect', hooks: {onBrokenMarkdownLinks: 'warn'}},
  themes: [
    '@docusaurus/theme-mermaid',
    [require.resolve('@easyops-cn/docusaurus-search-local'), {hashed: true, docsRouteBasePath: '/docs', indexBlog: false, indexPages: true, language: ['en'], highlightSearchTermsOnTargetPage: true, searchResultLimits: 12, searchResultContextMaxLength: 90, explicitSearchResultPath: true}],
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
      theme: {customCss: [require.resolve('katex/dist/katex.min.css'), './src/css/custom.css']},
    }],
  ],
  themeConfig: {
    mermaid: {options: {themeVariables: {fontSize: '22px'}, flowchart: {nodeSpacing: 40, rankSpacing: 50, padding: 12}}},
    colorMode: {defaultMode: 'dark', respectPrefersColorScheme: true},
    navbar: {
      title: 'Robotics & AI Bible',
      items: [
        {type: 'docSidebar', sidebarId: 'bible', position: 'left', label: 'Handbook'},
        {to: '/docs/glossary', label: 'Dictionary', position: 'left'},
        {to: '/docs/interview/question-bank', label: 'Interview Q&A', position: 'left'},
        {to: '/docs/reference/tools-libraries', label: 'Reference', position: 'left'},
        {to: '/docs/build-your-own/start-building', label: 'Build', position: 'left'},
        {to: '/docs/cheatsheets/formulas', label: 'Cheat Sheets', position: 'left'},
        {href: 'https://github.com/yeshwanthguru/Robotics_bible', label: 'GitHub', position: 'right'},
      ],
    },
    footer: {style: 'dark', copyright: 'Robotics & AI Bible: a personal handbook, dictionary and Q&A. Built with Docusaurus.'},
    docs: {sidebar: {hideable: true, autoCollapseCategories: true}},
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'python', 'cpp', 'matlab', 'r', 'yaml', 'lisp', 'cmake', 'json'],
    },
  },
};
export default config;
