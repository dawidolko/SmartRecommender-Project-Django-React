const fs = require("fs");
const path = require("path");

function walkSync(dir, callback) {
  const files = fs.readdirSync(dir);

  files.forEach((file) => {
    const filepath = path.join(dir, file);
    const stats = fs.statSync(filepath);

    if (stats.isDirectory()) {
      walkSync(filepath, callback);
    } else if (stats.isFile() && path.extname(filepath) === ".scss") {
      callback(filepath);
    }
  });
}

function updateSassImports(filePath) {
  let content = fs.readFileSync(filePath, "utf8");

  if (content.includes("@import")) {
    content = content.replace(
      /@import ["'](.+?)\.scss["'];/g,
      '@use "$1" as *;'
    );
    content = content.replace(/@import ["'](.+?)["'];/g, '@use "$1" as *;');

    fs.writeFileSync(filePath, content, "utf8");
  }
}

walkSync("src", updateSassImports);
