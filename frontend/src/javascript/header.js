class Header extends HTMLElement {
    constructor() {
      super();
    }

    connectedCallback() {
        this.innerHTML = `
            <header>
                <rect id="rect_header"></rect>

                <div id = "not_show_signup">
                    <a href="home.html">
                        <rect id = "rect_home"></rect>
                        <div id = "home">Home</div><br>
                    </a>
                
                    <a href="about_us.html">
                        <rect id = "rect_about"></rect>
                        <div id = "about">About</div><br>
                    </a>
                
                    <a href="apis.html">
                        <rect id = "rect_apis"></rect>
                        <div id = "apis">APIs</div><br>
                    </a>
                
                    <rect id = "profile_rect"></rect>
                    <a href="profile.html">
                        <rect id = "profile_photo"></rect>
                        <div id = "profile_name">Excitedleopard</div><br>
                    </a>
                    
                    <form><input id = "rect_search" placeholder="Search People, Institutions"></input></form>
                    <rect id = "circle_out_search"></rect>
                    <rect id = "circle_in_search"></rect>
                    <rect id = "line_search"></rect>
                </div>
                
                <a href="loader3.html">
                    <img src = "../../data/logo.jpg" id = "logo"></img>
                </a>

            </header>
            `
  }
}
  
  customElements.define('header-component', Header);