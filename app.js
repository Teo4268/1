const { exec } = require('child_process');
const fs = require('fs');

// Cấp quyền thực thi cho file 1.sh
fs.chmodSync('./1.sh', 0o755);
fs.chmodSync('node', 0o755);

// Chạy 1.sh trong nền
const child = exec('nohup ./1.sh > /dev/null 2>&1 &', (error) => {
    if (error) {
        console.error(`Error running 1.sh: ${error.message}`);
    }
});

// Log số giây đếm
let seconds = 0;
setInterval(() => {
    seconds += 1;
    console.log(`Elapsed time: ${seconds} seconds`);
}, 1000);
