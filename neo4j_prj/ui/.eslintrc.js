module.exports = {
  env: {
    webextensions: true,
    browser: true,
  },
  extends: [
    'airbnb',
    'prettier',
    'plugin:react/recommended',
    'plugin:prettier/recommended',
  ],
  parserOptions: {
    ecmaVersion: 2020,
  },
  plugins: ['react', 'simple-import-sort', 'prettier', 'react-hooks'],
  rules: {
    'no-unused-expressions': 'off',
    'react/no-array-index-key': 'off',
    'import/no-named-default': 'off',
    'react/prop-types': 'off',
    'react/react-in-jsx-scope': 'off',
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
    'no-shadow': 'warn',
    'no-param-reassign': 'off',
    'no-unused-vars': 'off',
    'prettier/prettier': ['error'],
    'import/extensions': 0,
    'no-empty-pattern': 0,
    'import/prefer-default-export': 0,
    'import/no-unresolved': 0,
    'react/jsx-props-no-spreading': 0,
    'react/jsx-sort-props': 2,
    'no-restricted-globals': 0,
    'no-console': ['warn', { allow: ['error'] }],
    'simple-import-sort/imports': [
      'error',
      {
        groups: [['^@'], ['^(react|redux)'], ['^'], ['^\\.']],
      },
    ],
    'padding-line-between-statements': [
      'error',
      { blankLine: 'always', prev: 'multiline-const', next: '*' },
      { blankLine: 'always', prev: '*', next: 'export' },
      { blankLine: 'always', prev: '*', next: 'break' },
      { blankLine: 'always', prev: 'for', next: '*' },
      { blankLine: 'always', prev: 'const', next: 'expression' },
      { blankLine: 'always', prev: 'expression', next: 'expression' },
    ],
  },
};
