const express = require("express");
const path = require("path");
const multer = require("multer");

const listenPort = 8080;
const app = express();
const uploadDir = __dirname + "/" + uploadDir; //"uploads"

// View Engine Setup
app.set("views",path.join(__dirname,"views"));
app.set("view engine", "ejs");

   
var storage = multer.diskStorage({
    destination: uploadDir,
    filename: function (req, file, cb) {
	cb(null, file.originalname);
    }
});
    
var upload = multer({ 
    storage: storage,
}).single("myfile");


app.get("/", function(req, res){
    res.render("upload");
})

app.post("/uploadFile",function (req, res, next) {
    // Error MiddleWare for multer file upload, so if any
    // error occurs, the image would not be uploaded!
    upload(req, res,function(err) {
        if(err) {
            // ERROR occured (here it can be occured due
            // to uploading image of size greater than
            // 1MB or uploading different file type)
            res.send(err);
        }
        else {
            // SUCCESS, image successfully uploaded
            res.render("success");
        }
    });
});

if (!path.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, 0744);
}

app.listen(listenPort, '0.0.0.0', function(error) {
    if(error) {
	throw error;
    }
    console.log("Server created Successfully on PORT %d", listenPort);
})
