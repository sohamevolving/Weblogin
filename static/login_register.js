document.querySelector(".log-in").addEventListener("click", function() {
    document.querySelector(".signIn").classList.add("active-dx");
    document.querySelector(".signUp").classList.add("inactive-sx");
    document.querySelector(".signUp").classList.remove("active-sx");
    document.querySelector(".signIn").classList.remove("inactive-dx");
});

document.querySelector(".back").addEventListener("click", function() {
    document.querySelector(".signUp").classList.add("active-sx");
    document.querySelector(".signIn").classList.add("inactive-dx");
    document.querySelector(".signIn").classList.remove("active-dx");
    document.querySelector(".signUp").classList.remove("inactive-sx");
});
