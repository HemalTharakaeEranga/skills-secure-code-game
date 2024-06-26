const express = require("express");
const bodyParser = require("body-parser");
const libxmljs = require("libxmljs");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const { exec } = require("child_process");
const app = express();

app.use(bodyParser.json());
app.use(bodyParser.text({ type: "application/xml" }));

const storage = multer.memoryStorage();
const upload = multer({ storage });

app.post("/ufo/upload", upload.single("file"), (req, res) => {
  if (!req.file) {
    return res.status(400).send("No file uploaded.");
  }

  console.log("Received uploaded file:", req.file.originalname);

  const uploadedFilePath = path.join(__dirname, req.file.originalname);
  fs.writeFileSync(uploadedFilePath, req.file.buffer);

  res.status(200).send("File uploaded successfully.");
});

app.post("/ufo", (req, res) => {
  const contentType = req.headers["content-type"];

  if (contentType === "application/json") {
      console.log("Received JSON data:", req.body);
      res.status(200).json({ ufo: "Received JSON data from an unknown planet." });
  } else if (contentType === "application/xml") {
      try {
          // Check if the request body starts with an XML tag
          if (!req.body.trim().startsWith("<")) {
              throw new Error("Start tag expected, '<' not found");
          }

          const xmlDoc = libxmljs.parseXml(req.body, {
              replaceEntities: false, // Disable entity replacement
              preserveWhitespace: true, // Preserve whitespace
              explicitArray: false, // Disable explicit array creation
              normalize: true, // Normalize whitespace and remove redundant nodes
              normalizeTags: true, // Normalize tag names
              recovery: true, // Enable recovery mode to handle invalid XML
              xmlns: true, // Enable XML namespaces
          });

          console.log("Received XML data from XMLon:", xmlDoc.toString());

          const extractedContent = [];

          xmlDoc
              .root()
              .childNodes()
              .forEach((node) => {
                  if (node.type() === "element") {
                      extractedContent.push(node.text());
                  }
              });

          if (
              req.body.includes('SYSTEM "') &&
              req.body.includes(".admin")
          ) {
              console.error("Blocked attempt to access .admin file");
              res.status(400).send("Invalid XML: Malicious attempt detected.");
              return;
          } else {
              res
                  .status(200)
                  .set("Content-Type", "text/plain")
                  .send(extractedContent.join(" "));
          }
      } catch (error) {
          console.error("XML parsing or validation error:", error.message);
          res.status(400).send("Invalid XML: " + error.message);
      }
  } else {
      res.status(405).send("Unsupported content type");
  }
});


const PORT = process.env.PORT || 3000;
const server = app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

module.exports = server;
