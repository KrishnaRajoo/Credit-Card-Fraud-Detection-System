window.addEventListener("scroll",()=>{

    let scrollTop=document.documentElement.scrollTop;

    let height=document.documentElement.scrollHeight-document.documentElement.clientHeight;

    let progress=(scrollTop/height)*100;

    document.getElementById("progress-bar").style.width=progress+"%";

});

// Counter Animation


const counters =
document.querySelectorAll(".counter");


counters.forEach(counter=>{


    counter.innerText="0";


    const update=()=>{


        const target =
        +counter.dataset.target;


        const value =
        +counter.innerText;


        const increment =
        target/100;



        if(value < target){


            counter.innerText =
            Math.ceil(value+increment);


            setTimeout(update,20);


        }


        else{


            counter.innerText =
            target.toLocaleString();


        }



    }


    update();


});

// =====================================
// Mobile Hamburger Menu
// =====================================


const hamburger =
document.getElementById(
"hamburger"
);


const navLinks =
document.getElementById(
"nav-links"
);



hamburger.addEventListener(
"click",
()=>{


    navLinks.classList.toggle(
        "active"
    );


    hamburger.classList.toggle(
        "open"
    );


});





// Close menu after clicking link


document
.querySelectorAll(
"#nav-links a"
)
.forEach(link=>{


    link.addEventListener(
    "click",
    ()=>{


        navLinks
        .classList
        .remove(
            "active"
        );


    });


});