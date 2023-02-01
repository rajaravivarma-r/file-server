class UploadFile {
  constructor(file, targetDirectory = null) {
    this.file = file;
    this.targetDirectory = targetDirectory;
    this.progressBar = this._createProgressBar();
    this.status = document.createElement("h3");
    this.loadedInTotal = document.createElement("p");
    this.progressStatusSection = document.createElement("div");

    this.progressStatusSection.appendChild(this.progressBar);
    this.progressStatusSection.appendChild(this.status);
    this.progressStatusSection.appendChild(this.loadedInTotal);
  }

  upload = (form) => {
    form.appendChild(this.progressStatusSection);
    let formdata = new FormData();
    formdata.append("upload", this.file);
    if (this.targetDirectory) {
      formdata.append("target_directory", this.targetDirectory);
    }
    let ajax = new XMLHttpRequest();
    ajax.upload.addEventListener("progress", this._progressHandler, false);

    let promise = new Promise((resolve, reject) => {
      const completeCallback = (event) => {
        this._completeHandler(event);
        resolve(form);
      };

      const errorCallback = (event) => {
        this._errorHandler(event);
        reject(form);
      };

      const abortCallback = (event) => {
        this._abortHandler(event);
        reject(form);
      };

      ajax.addEventListener("load", completeCallback, false);
      ajax.addEventListener("error", errorCallback, false);
      ajax.addEventListener("abort", abortCallback, false);
    });
    ajax.open("POST", "/upload");
    ajax.send(formdata);
    return promise;
  };

  _progressHandler = (event) => {
    const progress = "Uploaded " + event.loaded + " bytes of " + event.total;
    this.loadedInTotal.innerHTML = progress;
    const percent = (event.loaded / event.total) * 100;
    this.progressBar.value = Math.round(percent);
    const uploadStatus = Math.round(percent) + "% uploaded... please wait";
    this.status.innerHTML = uploadStatus;
  };

  _completeHandler = (event) => {
    // document.getElementById("status").innerHTML = event.target.responseText;
    this.status.innerHTML = event.target.responseText;
  };

  _errorHandler = (event) => {
    // document.getElementById("status").innerHTML = "Upload Failed";
    this.status.innerHTML = "Upload Failed";
  };

  _abortHandler = (event) => {
    // document.getElementById("status").innerHTML = "Upload Aborted";
    // document.getElementById("status").innerHTML = "Ready!";
    this.status.innerHTML = "Upload Aborted! Now Ready for new uploads!";
  };

  _resetProgressInformation = () => {
    // document.getElementById("progressBar").value = 0;
    this.progressBar.value = 0;
  };

  _createProgressBar = () => {
    let progressBar = document.createElement("progress");
    progressBar.value = 0;
    progressBar.max = 100;
    progressBar.style = "width: 90%; margin: auto";
    return progressBar;
  };
}

function uploadFile() {
  let files = document.getElementById("upload_file").files;
  let targetDirectory = document.getElementById("target_directory").value;
  let promises = [];
  for (let i = 0; i < files.length; i += 1) {
    const uploadFile = new UploadFile(files[i], targetDirectory);
    promises.push(uploadFile.upload(document.getElementById("upload_form")));
  }
  Promise.all(promises).then(
    (forms) => {
      forms[0].reset();
    },
    (forms) => {
      console.log("Error!");
    }
  );
}
