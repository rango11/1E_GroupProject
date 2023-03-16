// document.getElementById("toggle-sidebar").addEventListener("click", function() {
//     const sidebar = document.getElementById("sidebar");
//     const toggleIcon = document.querySelector(".toggle-icon");
//     console.log("button pressed")
//     if (sidebar.style.left === "0px") {
//       sidebar.style.left = "-250px";
//       toggleIcon.innerHTML = "&rsaquo;";
//     } else {
//       sidebar.style.left = "0px";
//       toggleIcon.innerHTML = "&lsaquo;";
//     }
//   });


// document.getElementById("toggle-sidebar").addEventListener("click", function() {
//     const sidebar = document.getElementById("sidebar");
//     const toggleButton = document.getElementById("toggle-sidebar");
//     const toggleIcon = document.querySelector(".toggle-icon");
    
//     if (sidebar.style.left === "0px") {
//       sidebar.style.left = "-250px";
//       toggleButton.style.left = "0px";
//       toggleIcon.innerHTML = "&rsaquo;";
//     } else {
//       sidebar.style.left = "0px";
//       toggleButton.style.left = "250px";
//       toggleIcon.innerHTML = "&lsaquo;";
//     }
//   });

document.getElementById("toggle-sidebar").addEventListener("click", function() {
    const sidebar = document.getElementById("sidebar");
    const toggleButton = document.getElementById("toggle-sidebar");
    
    if (sidebar.style.left === "0px") {
      sidebar.style.left = "-250px";
      toggleButton.style.left = "0px";
      toggleButton.classList.remove("opened");
    } else {
      sidebar.style.left = "0px";
      toggleButton.style.left = "250px";
      toggleButton.classList.add("opened");
    }
  });