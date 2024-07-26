module.exports = {
  apps: [
    {
      name: "fastapi-summarizer",
      script: "main.py",
      interpreter: "python3",
      env: {
        NODE_ENV: "development",
      },
      env_production: {
        NODE_ENV: "production",
      },
    },
  ],
};
