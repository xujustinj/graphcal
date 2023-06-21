module.exports = {
    parser: "@typescript-eslint/parser",
    plugins: ["@typescript-eslint", "react", "react-hooks", "eslint-plugin-import", "prettier"],
    env: {
        browser: true
    },
    extends: [
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended",
        "plugin:react/recommended",
        "plugin:prettier/recommended"
    ],
    parserOptions: {
        project: ["tsconfig.json"],
        ecmaVersion: 2020,
        tsconfigRootDir: __dirname,
        sourceType: "module",
        ecmaFeatures: {
            jsx: true
        }
    },
    rules: {
        "@typescript-eslint/explicit-function-return-type": "off",
        "@typescript-eslint/no-unused-vars": ["warn", {ignoreRestSiblings: true}],
        "react/jsx-filename-extension": [
            "warn",
            {
                extensions: [".jsx", ".tsx"]
            }
        ],
        "react/prop-types": "off",
        "react-hooks/rules-of-hooks": "error",
        "react-hooks/exhaustive-deps": "warn",
        "no-shadow": ["error", {builtinGlobals: false, hoist: "functions", allow: []}]
    },
    settings: {
        react: {
            version: "detect"
        }
    },
    ignorePatterns: [".eslintrc.js"] // see https://stackoverflow.com/a/75791515
};
