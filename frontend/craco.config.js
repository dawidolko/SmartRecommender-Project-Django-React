module.exports = {
  webpack: {
    configure: (webpackConfig) => {
      const sassRule = webpackConfig.module.rules
        .find((rule) => rule.oneOf)
        ?.oneOf?.find(
          (rule) => rule.test && rule.test.toString().includes("scss|sass")
        );

      if (sassRule) {
        const sassLoader = sassRule.use?.find(
          (loader) => loader.loader && loader.loader.includes("sass-loader")
        );

        if (sassLoader) {
          sassLoader.options = {
            ...sassLoader.options,
            sassOptions: {
              ...sassLoader.options?.sassOptions,
              silenceDeprecations: ["legacy-js-api"],
            },
          };
        }
      }

      return webpackConfig;
    },
  },
};
