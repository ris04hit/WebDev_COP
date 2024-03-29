class Header extends HTMLElement {
    constructor() {
      super();
    }

    connectedCallback() {
        this.innerHTML = `
 
        <header id = "desktop_header">
            <rect id="rect_header">
            <div id = "not_show_signup">
                <a href="{{url_for('home')}}">
                    <rect id = "rect_home"></rect>
                    <div id = "home">Home</div><br>
                </a>
            
                <a href="{{url_for('about')}}">
                    <rect id = "rect_about"></rect>
                    <div id = "about">About</div><br>
                </a>
            
                <a href="{{url_for('apis')}}">
                    <rect id = "rect_apis"></rect>
                    <div id = "apis">APIs</div><br>
                </a>
            
                <rect id = "profile_rect">
                    
                </rect>
                <a href="{{url_for('profile', username = username)}}">
                   <img id = "profile_photo" src="{{ url_for('profile_photo') }}">
                    <div id = "profile_name">{{username}}</div><br>
                </a>
                
                <form><input id = "rect_search" placeholder="Search People, Institutions"></input></form>
                <div id = "search_result_rect" class="search_rect pop_up">
                <div id="search_result_entry"></div>
                </div>
            </div>
            
            <a href="{{url_for('loader3')}}">
                <img src = "{{url_for('static',filename='/data/logo.jpg')}}" id = "logo"></img>
            </a>
            </rect>
        </header>
            `
  }
}
  
  customElements.define('header-component', Header);