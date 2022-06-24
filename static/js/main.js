// start of the sidenav js
function openNav() {
    document.getElementById("mySidenav").style.animation = "expand 0.3s forwards";
    document.getElementById("closeBtn").style.display = "block";
    document.getElementById("closeBtn").style.animation = "show 0.3s";
    // page-overlay
    document.getElementById("page-overlay").style.display = "block";
    document.getElementById("page-overlay").style.animation = "show 0.3s";
  }
  
  function closeNav() {
    document.getElementById("mySidenav").style.animation = "collapse 0.3s forwards";
    document.getElementById("closeBtn").style.animation = "hide 0.3s";
    // page-overlay
    document.getElementById("page-overlay").style.animation = "hide 0.3s";
  
    setTimeout(() => {
      document.getElementById("closeBtn").style.display = "none";
      document.getElementById("page-overlay").style.display = "none";
  }, 300);
  }
  // end of the sidenav js