module.exports = {
  apps: [
    {
      name: 'vert.duz.ie',
      port: '3001',
      exec_mode: 'cluster',
      instances: 'max',
      script: './.output/server/index.mjs'
    }
  ]
};
