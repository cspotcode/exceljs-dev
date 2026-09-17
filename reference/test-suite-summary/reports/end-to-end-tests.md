# End-to-end tests (`npm run test:end-to-end`)

Command: `mocha --require spec/config/setup spec/end-to-end --recursive`

Location: `spec/end-to-end/**/*.spec.js`

To regenerate this listing without running assertions:
```
npx mocha --require spec/config/setup spec/end-to-end --recursive --dry-run --reporter spec --no-colors
```

```


  Express
    ✔ downloads a workbook


  1 passing (2ms)
```
