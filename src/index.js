class UploadFile {
  constructor(file) {
    this.file = file;
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
    let ajax = new XMLHttpRequest();
    ajax.upload.addEventListener("progress", this._progressHandler, false);
    ajax.addEventListener("load", this._completeHandler, false);
    ajax.addEventListener("error", this._errorHandler, false);
    ajax.addEventListener("abort", this._abortHandler, false);
    ajax.open("POST", "/upload");
    ajax.send(formdata);
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
  for(let i = 0; i < files.length; i += 1) {
    const uploadFile = new UploadFile(files[i]);
    uploadFile.upload(document.getElementById('upload_form'));
  }
}
