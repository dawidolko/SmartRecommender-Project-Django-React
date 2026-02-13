# react-router-scroll-to-top

[![npm Version](https://img.shields.io/npm/v/react-router-scroll-to-top.svg)](https://www.npmjs.com/package/react-router-scroll-to-top)
![npm downloads per week](https://img.shields.io/npm/dw/react-router-scroll-to-top)
![Minified size](https://img.shields.io/bundlephobia/min/react-router-scroll-to-top)
[![Open issues](https://img.shields.io/github/issues-raw/dimazuien/react-router-scroll-to-top)](https://github.com/dimazuien/react-router-scroll-to-top/issues)
[![Open pull requests](https://img.shields.io/github/issues-pr-raw/dimazuien/react-router-scroll-to-top)](https://github.com/dimazuien/react-router-scroll-to-top/pulls)
[![GitHub Stars](https://img.shields.io/github/stars/dimazuien/react-router-scroll-to-top)](https://github.com/dimazuien/react-router-scroll-to-top/stargazers)
![CircleCI status](https://img.shields.io/circleci/build/github/dimazuien/react-router-scroll-to-top/main?label=circleci)
![Code scanning](https://img.shields.io/github/workflow/status/dimazuien/react-router-scroll-to-top/CodeQL?label=code%20scanning)

ScrollToTop is a React component that scrolls to the top of a page when the current location gets changed. Since React Router doesn't provide out-of-the-box support for scroll restoration due to [browsers having started handling it on their own](https://majido.github.io/scroll-restoration-proposal/history-based-api.html), this package implements a component for scrolling to the top manually as it is given in [React Router docs](https://reactrouter.com/web/guides/scroll-restoration#scroll-restoration-scroll-to-top).

## Usage

```shell
npm install react-router-scroll-to-top
```

```jsx
import { ScrollToTop } from 'react-router-scroll-to-top';

const App = () => (
  <BrowserRouter>
    <ScrollToTop />
    <Routes>{/* routes */}</Routes>
  </BrowserRouter>
);
```

Read [the documentation](https://github.com/dimazuien/react-router-scroll-to-top/blob/main/docs/index.md) for more details. You can also play with a [demo](https://codesandbox.io/s/react-router-scroll-to-top-n1mg3).

## Support

If you like this package and want to support it, you can do it on [Patreon](https://www.patreon.com/dimazuien)
