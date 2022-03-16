const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar__menu');
const navLogo = document.querySelector('#navbar__logo');

$(document).ready(function() {
  $.ajax({
      url: "https://gbs-women-wellness.herokuapp.com/diseases"
  }).then(function(data) {
    console.log(document.querySelector(".services__wrapper"));
    document.querySelector(".services__wrapper").innerHTML=data.data.diseases.map(el=>`<div class="services__card">
    <h2>${el.name}</h2>
    <p>${el.description}</p>
    <div class="services__btn"><button><a href="details.html">Get Started</a></button></div>
  </div>`).join('');
    //  $('services__wrapper').innerWidth;
  });
  $.ajax({
    url: "https://gbs-women-wellness.herokuapp.com/tests"
}).then(function(data) {
  // console.log(document.querySelector(".services__wrapper"));
  document.querySelectorAll(".services__wrapper")[1].innerHTML=data.data.tests.map(el=>`<div class="services__card">
  <h2>${el.name}</h2>
  <p>${el.description.slice(0,200) }${(el.description.length>200?"...":"")}</p>
  <div class="services__btn"><button><a href="details.html">Get Started</a></button></div>
</div>`).join('');
});
});
// Display Mobile Menu
const mobileMenu = () => {
  menu.classList.toggle('is-active');
  menuLinks.classList.toggle('active');
};

menu.addEventListener('click', mobileMenu);

// Show active menu when scrolling
const highlightMenu = () => {
  const elem = document.querySelector('.highlight');
  const homeMenu = document.querySelector('#home-page');
  const aboutMenu = document.querySelector('#about-page');
  const servicesMenu = document.querySelector('#services-page');
  let scrollPos = window.scrollY;
  // console.log(scrollPos);

  // adds 'highlight' class to my menu items
  if (window.innerWidth > 960 && scrollPos < 600) {
    homeMenu.classList.add('highlight');
    aboutMenu.classList.remove('highlight');
    return;
  } else if (window.innerWidth > 960 && scrollPos < 1400) {
    aboutMenu.classList.add('highlight');
    homeMenu.classList.remove('highlight');
    servicesMenu.classList.remove('highlight');
    return;
  } else if (window.innerWidth > 960 && scrollPos < 2345) {
    servicesMenu.classList.add('highlight');
    aboutMenu.classList.remove('highlight');
    return;
  }

  if ((elem && window.innerWIdth < 960 && scrollPos < 600) || elem) {
    elem.classList.remove('highlight');
  }
};

window.addEventListener('scroll', highlightMenu);
window.addEventListener('click', highlightMenu);

//  Close mobile Menu when clicking on a menu item
const hideMobileMenu = () => {
  const menuBars = document.querySelector('.is-active');
  if (window.innerWidth <= 768 && menuBars) {
    menu.classList.toggle('is-active');
    menuLinks.classList.remove('active');
  }
};

menuLinks.addEventListener('click', hideMobileMenu);
navLogo.addEventListener('click', hideMobileMenu);