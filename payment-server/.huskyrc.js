module.exports = {
  hooks: {
    'pre-commit': 'yarn ts-check && yarn concurrently \"yarn lint:style\" \"yarn lint-fix\"'
  }
}
