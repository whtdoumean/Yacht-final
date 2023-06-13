// burger menu

const iconMenu = document.querySelector(".menu-icon");
const menuBody = document.querySelector(".menu-body");
if (iconMenu) {
    iconMenu.addEventListener("click", toggleMenu);

    function toggleMenu(e) {
        if (!menuBody.classList.contains("_active")) {
            openMenu();
        } else if (menuBody.classList.contains("_active")) {
            closeMenu();
        }
    }
}

function openMenu() {
    if (!menuBody.classList.contains("_active") && !iconMenu.classList.contains("_active")) {
        menuBody.classList.add("_active");
        iconMenu.classList.add("_active");
        html.classList.add("lock");
    }
}

function closeMenu() {
    if (menuBody.classList.contains("_active") && iconMenu.classList.contains("_active")) {
        menuBody.classList.remove("_active");
        iconMenu.classList.remove("_active");
        html.classList.remove("lock");
    }
}


// header hide when scrolling

let lastScroll = 0;
const defoultOffset = 500;
const header = document.querySelector('.header');

const scrollPosition = () => window.pageYOffset || document.documentElement.scrollTop;
const containHide = () => header.classList.contains('hide');

window.addEventListener('scroll', () => {

    if (scrollPosition() > lastScroll && !containHide() && scrollPosition() > defoultOffset) {
        //scroll down
        header.classList.add('hide');
    }
    else if (scrollPosition() < lastScroll && containHide()) {
        //scroll up
        header.classList.remove('hide');
    }

    lastScroll = scrollPosition();

});


// scrolling on link click

const scrollingLinks = document.querySelectorAll(".scroll-to[data-goto]");
scrollingLinks.forEach(scrollingLink => {
    console.log(scrollingLink);
});

if (scrollingLinks.length > 0) {
    scrollingLinks.forEach(scrollingLink => {
        scrollingLink.addEventListener("click", onScrollingLinklClick);
    });

    function onScrollingLinklClick(e) {
        const scrollingLink = e.target;
        if (scrollingLink.dataset.goto && document.querySelector(scrollingLink.dataset.goto)) {
            const gotoBlock = document.querySelector(scrollingLink.dataset.goto);
            //const gotoBlockValue = gotoBlock.getBoundingClientRect().top + scrollY - document.querySelector(".header").offsetHeight;
            const gotoBlockValue = gotoBlock.getBoundingClientRect().top + scrollY - (document.documentElement.clientWidth / 10);

            closeMenu();

            window.scrollTo({
                top: gotoBlockValue,
                behavior: "smooth"
            });
        }
        e.preventDefault();
    }
}


//open popups

const popupLinks = document.querySelectorAll('.popup-link[data-popupname]');
popupLinks.forEach(popupLink => {
    console.log(popupLink);
});
const body = document.querySelector('body');
const wrapper = document.querySelector(".wrapper");
const html = document.querySelector("html");
const lockPadding = document.querySelectorAll('.lock-padding');

let unlock = true;

const timeout = 500;

if (popupLinks.length > 0) {
    for (let index = 0; index < popupLinks.length; index++) {
        const popupLink = popupLinks[index];
        popupLink.addEventListener("click", function (e) {
            const popupName = document.querySelector(popupLink.dataset.popupname);
            //const curentPopup = document.getElementById(popupName);
            //popupOpen(curentPopup);
            popupOpen(popupName);
            e.preventDefault();
        });
    }
}

const popupCloseIcons = document.querySelectorAll(".close-popup");
if (popupCloseIcons.length > 0) {
    for (let index = 0; index < popupCloseIcons.length; index++) {
        const popupCloseIcon = popupCloseIcons[index];
        popupCloseIcon.addEventListener("click", function (e) {
            popupClose(popupCloseIcon.closest(".popup"));
            e.preventDefault();
        });
    }
}

function popupOpen(curentPopup) {
    if (curentPopup && unlock) {
        const popupActive = document.querySelector(".popup.open");
        if (popupActive) {
            popupClose(popupActive, false);
        } else {
            bodyLock();
        }
        curentPopup.classList.add("open");
        curentPopup.addEventListener("click", function (e) {
            if (!e.target.closest(".popup-content")) {
                popupClose(e.target.closest(".popup"));
            }
        });
    }
}

function popupClose(popupActive, doUnlock = true) {
    if (unlock) {
        popupActive.classList.remove("open");
        if (doUnlock) {
            bodyUnlock();
        }
    }
}

function bodyLock() {
    const lockPaddingValue = window.innerWidth - document.querySelector(".wrapper").offsetWidth + "px";
    if (lockPadding.length > 0) {
        for (let index = 0; index < lockPadding.length; index++) {
            const el = lockPadding[index];
            el.style.paddingRight = lockPaddingValue;
        }
    }

    //body.style.paddingRight = lockPaddingValue;
    //body.classList.add("lock");
    //wrapper.style.paddingRight = lockPaddingValue;
    //wrapper.classList.add("lock");
    html.style.paddingRight = lockPaddingValue;
    html.classList.add("lock");

    unlock = false;
    setTimeout(function () {
        unlock = true;
    }, timeout);
}

function bodyUnlock() {
    setTimeout(function () {
        for (let index = 0; index < lockPadding.length; index++) {
            const el = lockPadding[index];
            el.style.paddingRight = "0px";
        }
        //body.style.paddingRight = "0px";
        //body.classList.remove("lock");
        //wrapper.style.paddingRight = "0px";
        //wrapper.classList.remove("lock");
        html.style.paddingRight = "0px";
        html.classList.remove("lock");
    }, timeout);

    unlock = false;
    setTimeout(function () {
        unlock = true;
    }, timeout);
}

document.addEventListener("keydown", function (e) {
    if (e.which === 27) {
        const popupActive = document.querySelector(".popup.open");
        popupClose(popupActive);
    }
});

// carousel
let offsetEvrika = 0;
let photoWidth = document.querySelector('.carousel').offsetWidth;
const photoList = document.querySelectorAll('.carousel-photo');
const sliderLineEvrika = document.querySelector('.sliderline-evrika');

for (let i = 0; i < photoList.length; i++) {
    const photo = photoList[i];
    photo.style.width = photoWidth + 'px';
};

document.querySelector('.slider-next-evrika').addEventListener('click', function () {
    offsetEvrika = offsetEvrika + photoWidth;
    if (offsetEvrika > photoWidth * 3) {
        offsetEvrika = 0;
    };
    const photoList = document.querySelectorAll('.carousel-photo');
    for (let i = 0; i < photoList.length; i++) {
        const photo = photoList[i];
        photo.style.width = photoWidth + 'px';
    };
    sliderLineEvrika.style.left = -offsetEvrika + 'px';
});

document.querySelector('.slider-prev-evrika').addEventListener('click', function () {
    offsetEvrika = offsetEvrika - photoWidth;
    if (offsetEvrika < 0) {
        offsetEvrika = photoWidth * 3;
    };
    const photoList = document.querySelectorAll('.carousel-photo');
    for (let i = 0; i < photoList.length; i++) {
        const photo = photoList[i];
        photo.style.width = photoWidth + 'px';
    };
    sliderLineEvrika.style.left = -offsetEvrika + 'px';
});

let offsetGold = 0;
const sliderLineGold = document.querySelector('.sliderline-gold');

document.querySelector('.slider-next-gold').addEventListener('click', function () {
    offsetGold = offsetGold + photoWidth;
    if (offsetGold > photoWidth * 5) {
        offsetGold = 0;
    };
    const photoList = document.querySelectorAll('.carousel-photo');
    for (let i = 0; i < photoList.length; i++) {
        const photo = photoList[i];
        photo.style.width = photoWidth + 'px';
    };
    sliderLineGold.style.left = -offsetGold + 'px';
});

document.querySelector('.slider-prev-gold').addEventListener('click', function () {
    offsetGold = offsetGold - photoWidth;
    if (offsetGold < 0) {
        offsetGold = photoWidth * 5;
    };
    const photoList = document.querySelectorAll('.carousel-photo');
    for (let i = 0; i < photoList.length; i++) {
        const photo = photoList[i];
        photo.style.width = photoWidth + 'px';
    };
    sliderLineGold.style.left = -offsetGold + 'px';
});


// phone mask
$(function () {
    //2. Получить элемент, к которому необходимо добавить маску
    $("#phone-number").mask("999 999 99 99", { placeholder: " " });
});


//form 

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form");
    form.addEventListener("submit", formSend);

    async function formSend(e) {
        e.preventDefault();

        let error = formValidate(form);
        let formData = new FormData(form);

        if (error === 0) {
            form.parentElement.classList.add("_sending");
            let response = await fetch('/postemail', {
                method: 'POST',
                body: formData
            });
            if (response.ok) {
                let result = await response.json();
                form.reset();
                setTimeout(() => {  form.parentElement.classList.remove("_sending"); }, 500);
                setTimeout(() => {  form.parentElement.classList.add("_done"); }, 300);
                // setTimeout(() => {  form.parentElement.classList.remove("_done"); }, 1700);
            } else {
                alert("Ошибка")
                form.parentElement.classList.remove("_sending");
            }
        } else {
            //pass
        }

    }

    function formValidate(form) {
        let error = 0;
        let formReq = document.querySelectorAll("._req");
        for (let index = 0; index < formReq.length; index++) {
            const input = formReq[index];
            formRemoveError(input);

            if (input.classList.contains("._phone")) {
                if (phoneTest(input)) {
                    formAddError(input);
                    error++;
                }
            } else if (input.getAttribute("type") === "checkbox" && input.checked === false) {
                formAddError(input);
                error++;
            } else {
                if (input.value === "") {
                    formAddError(input);
                    error++;
                }
            }
        }
        return error;
    }
    function formAddError(input) {
        input.parentElement.classList.add("_error");
        input.classList.add("_error");
    }
    function formRemoveError(input) {
        input.parentElement.classList.remove("_error");
        input.classList.remove("_error");
    }
    function phoneTest(input) {
        return String(input).length < 9;
    }
});

