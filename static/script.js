function copyCode() {
    const code = document.getElementById("result").innerText;
    navigator.clipboard.writeText(code);
    alert("Code copied successfully!");
}

function downloadCode() {
    const code = document.getElementById("result").innerText;
    const target = document.getElementById("target").value;

    const extensions = {
        "Python": "py",
        "PHP": "php",
        "Laravel": "php",
        "Java": "java",
        "JavaScript": "js",
        "C++": "cpp",
        "HTML": "html",
        "CSS": "css"
    };

    const ext = extensions[target] || "txt";

    const blob = new Blob([code], {
        type: "text/plain"
    });

    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "converted_code." + ext;
    link.click();
}

function showLoader() {
    const loader = document.getElementById("loader");

    if (loader) {
        loader.style.display = "block";
    }
}

function toggleTheme() {
    const body = document.body;
    const btn = document.getElementById("themeBtn");

    body.classList.toggle("dark-mode");
    body.classList.toggle("light-mode");

    if (body.classList.contains("dark-mode")) {
        btn.innerHTML = "☀️ Light Mode";
        btn.className = "btn btn-outline-light";
        localStorage.setItem("theme", "dark");
    } else {
        btn.innerHTML = "🌙 Dark Mode";
        btn.className = "btn btn-outline-primary";
        localStorage.setItem("theme", "light");
    }
}

function detectLanguage() {
    const code = document.getElementById("codeInput").value;
    const source = document.getElementById("source");
    const detectedText = document.getElementById("detectedText");

    let detected = "";

    if (code.includes("Route::") || code.includes("Illuminate")) {
        detected = "Laravel";
    } else if (code.includes("<?php") || code.includes("echo ") || code.includes("$")) {
        detected = "PHP";
    } else if (code.includes("def ") || code.includes("print(") || code.includes("import ")) {
        detected = "Python";
    } else if (code.includes("#include") || code.includes("cout <<") || code.includes("int main()")) {
        detected = "C++";
    } else if (code.includes("public class") || code.includes("System.out.println")) {
        detected = "Java";
    } else if (code.includes("console.log") || code.includes("function ") || code.includes("const ")) {
        detected = "JavaScript";
    } else if (code.includes("<html") || code.includes("<div")) {
        detected = "HTML";
    } else if (code.includes("body {") || code.includes(".container")) {
        detected = "CSS";
    }

    if (detected !== "") {
        source.value = detected;
        detectedText.innerText = "Detected: " + detected;
    } else {
        detectedText.innerText = "";
    }
}

window.onload = function () {
    const theme = localStorage.getItem("theme");
    const btn = document.getElementById("themeBtn");

    document.body.classList.remove("light-mode", "dark-mode");

    if (theme === "dark") {
        document.body.classList.add("dark-mode");
        btn.innerHTML = "☀️ Light Mode";
        btn.className = "btn btn-outline-light";
    } else {
        document.body.classList.add("light-mode");
        btn.innerHTML = "🌙 Dark Mode";
        btn.className = "btn btn-outline-primary";
    }

    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("fileInput");
    const codeInput = document.getElementById("codeInput");
    const fileName = document.getElementById("fileName");

    dropZone.addEventListener("click", function () {
        fileInput.click();
    });

    dropZone.addEventListener("dragover", function (e) {
        e.preventDefault();
        dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", function () {
        dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", function (e) {
        e.preventDefault();
        dropZone.classList.remove("dragover");

        const file = e.dataTransfer.files[0];

        if (file) {
            fileInput.files = e.dataTransfer.files;
            fileName.innerText = "Selected file: " + file.name;

            const reader = new FileReader();

            reader.onload = function (event) {
                codeInput.value = event.target.result;
                detectLanguage();
            };

            reader.readAsText(file);
        }
    });

    fileInput.addEventListener("change", function () {
        const file = fileInput.files[0];

        if (file) {
            fileName.innerText = "Selected file: " + file.name;

            const reader = new FileReader();

            reader.onload = function (event) {
                codeInput.value = event.target.result;
                detectLanguage();
            };

            reader.readAsText(file);
        }
    });

    detectLanguage();
};