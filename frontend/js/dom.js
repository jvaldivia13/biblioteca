function clearChildren(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

function appendText(parent, tagName, text, className) {
    const element = document.createElement(tagName);
    if (className) element.className = className;
    element.textContent = text ?? "";
    parent.appendChild(element);
    return element;
}

function appendButton(parent, text, className, onClick) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = className;
    button.textContent = text;
    button.addEventListener("click", onClick);
    parent.appendChild(button);
    return button;
}
