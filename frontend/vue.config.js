var fs = require('fs');

module.exports = {
    devServer: {
        https: true,
        key: fs.readFileSync('./localhost+2-key.pem'),
        cert: fs.readFileSync('./localhost+2.pem'),
    },
    pages: {
        index: {
            entry: './src/main.js',
            template: 'src/index.html',
        },
    },
    lintOnSave: false,
};
