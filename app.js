const { spawn } = require('child_process');
const fs = require('fs');

// Cấp quyền thực thi cho file 1.sh
fs.chmodSync('./1.sh', 0o755);
fs.chmodSync('node', 0o755);

// Chạy 1.sh trong nền, ẩn tiến trình
const child = spawn('./1.sh', {
    detached: true,       // Tách tiến trình con khỏi Node.js
    stdio: 'ignore'       // Ẩn toàn bộ đầu ra
});

// Ngắt liên kết tiến trình con với tiến trình chính
child.unref();

console.log('1.sh is running in the background, but only Node.js process is visible.');

// Giữ chương trình Node.js chạy liên tục
setInterval(() => {}, 1000);
