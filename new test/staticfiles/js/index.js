
/*---------(Page transitions and Smooth Scrolling)-----------------------------------------*/

//smooth scroll using GSAP + Locomotive Scroll
const locScroll = new LocomotiveScroll({
    el:document.querySelector("[data-scroll-container]"),
    smooth:true
})

//article cards fade-in transition using GSAP
gsap.from(".article_card, .package_card, .dashboard_card", {duration: 1, opacity:0, y:80, stagger:.2})

//page transition-1 using GSAP
gsap.from("[data-transition]", {duration: .5, opacity:0, y:50})



/*---------(EditorJS text editor in Setup-2)-----------------------------------------*/

//text editor for Article Body on Setup-2 using EditorJS
const editor = new EditorJS({
    holder: "editorjs"
})

//update locScroll when Article Body height changes
document.getElementById("editorjs").addEventListener('keyup', ()=>{
    locScroll.update()
})



/*----------------------------------------------------------------------------------*/