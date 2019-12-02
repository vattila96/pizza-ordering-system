module.exports = {
  moduleFileExtensions: ['js', 'ts', 'tsx'],
  transform: {
    '\\.(ts|tsx)$': 'ts-jest'
  },
  testEnvironment: 'node',
  modulePathIgnorePatterns: ['<rootDir>/dist/']
}
