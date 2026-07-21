const reveals =
document.querySelectorAll(".reveal");

function revealOnScroll(){

    const windowHeight =
    window.innerHeight;

    reveals.forEach(function(item){

        const top =
        item.getBoundingClientRect().top;

        if(top < windowHeight - 120){

            item.classList.add("active");

        }

    });

}

window.addEventListener(
"scroll",
revealOnScroll
);

window.addEventListener(
"load",
revealOnScroll
);