function include(file) {
    var script  = document.createElement('script');
    script.src  = file;
    script.type = 'text/javascript';
    script.defer = true;
    document.getElementsByTagName('head').item(0).appendChild(script);
  }

include("https://cdn.jsdelivr.net/npm/vue@2.5.13/dist/vue.js");
  include("https://cdnjs.cloudflare.com/ajax/libs/axios/0.21.1/axios.js");
  include("https://unpkg.com/v-tooltip@2.0.2");

    new Vue({

        el: '#nepenthes_search',
        delimiters: ['{[',']}'],
        data: {
          search_term: "Search for device",
          message: "dsdsas",
          nepenthes: [],
          selected_category: 'None',
          csrf_token: "",
            widht_limit: 575, // if it is equal smaller we use mobile filter
        },
        mounted: function() {
          this.getNepenthes();
        },
        methods: {
          getToken:function(){
            this.csrf_token = document.getElementById("csrf").value;
          },
          getNepenthes: function() {
              let flag = ""
            let api_base_url = '/api/nepenthes/';
            axios.get(api_base_url)
                .then((response) => {
                  this.nepenthes = response.data;
                })
          },
          getSearchResults: function() {
              let api_base_url = '/api/nepenthes/';

              let flag = ""
              let width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
              if(width <= this.widht_limit){
                  //molbile values
                  flag = "m_";
              }else{
                  // desktop values
                  flag = "";
              }

              let species = document.getElementById(flag+"species").checked;
              let hybrid = document.getElementById(flag+"hybrid").checked;
              let male = document.getElementById(flag+"male").checked;
              let female = document.getElementById(flag+"female").checked;
              let blooming = document.getElementById(flag+"blooming").checked;
              let soon_blooming = document.getElementById(flag+"soon_blooming").checked;

              if(species == false && hybrid == true ){
                api_base_url +="?isHybrid="+0;
              }else if(species == true && species == false ){
                  api_base_url +="?isHybrid="+1;
              }

              if(male == false && female == true ){
                api_base_url +="?sex="+1;
              }else if(male == true && female == false){
                  api_base_url +="?sex="+0;
              }

              if(blooming == false && soon_blooming == true ){
                api_base_url +="?flower_status="+1;
              }else if(blooming == true && soon_blooming == false){
                  api_base_url +="?flower_status="+2;
              }
              console.log(api_base_url);

            axios.get(api_base_url)
                .then((response) => {
                  this.nepenthes = response.data;
                })
          },
        }
      });