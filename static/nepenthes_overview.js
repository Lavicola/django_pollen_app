function include(file) {
    var script = document.createElement('script');
    script.src = file;
    script.type = 'text/javascript';
    script.defer = true;
    document.getElementsByTagName('head').item(0).appendChild(script);
}

include("https://cdn.jsdelivr.net/npm/vue@2.5.13/dist/vue.js");
include("https://cdnjs.cloudflare.com/ajax/libs/axios/0.21.1/axios.js");
include("https://unpkg.com/v-tooltip@2.0.2");

new Vue({
    el: '#nepenthes_search',
    delimiters: ['{[', ']}'],
    data: {
        csrfTokenName: "csrftoken",
        all_nepenthes: [],
        nepenthes: [],
        widht_limit: 575, // if it is equal smaller we use mobile filter
    },
    mounted: function () {
        this.getNepenthes();
    },
    methods: {
        getToken: function (name) {
            // https://stackoverflow.com/a/15724300
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        },
        getUserNepenthes: function (id) {
            return document.getElementById("dropdown_" + id).value;


        },
        getNepenthes: function () {
            let flag = ""
            let api_base_url = '/api/nepenthes/';
            axios.get(api_base_url)
                .then((response) => {
                    this.all_nepenthes = response.data;
                    this.nepenthes = this.all_nepenthes;
                })
        },
        getSearchResults: function () {
            let flag = ""
            let width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
            if (width <= this.widht_limit) {
                //molbile values
                flag = "m_";
            } else {
                // desktop values
                flag = "";
            }

            let species = document.getElementById(flag + "species").checked;
            let hybrid = document.getElementById(flag + "hybrid").checked;
            let male = document.getElementById(flag + "male").checked;
            let female = document.getElementById(flag + "female").checked;
            let blooming = document.getElementById(flag + "blooming").checked;
            let soon_blooming = document.getElementById(flag + "soon_blooming").checked;

            let gender;
            let flower_status;
            let spec;

            if (species == false && hybrid == true) {
                spec = true;
            } else if (species == true && hybrid == false) {
                spec = false;
            } else {
                spec = DONT_CARE;
            }

            if (male == false && female == true) {
                gender = SEX.female;
            } else if (male == true && female == false) {
                gender = SEX.male;
            } else {
                gender = DONT_CARE // we don´t care
            }

            if (blooming == false && soon_blooming == true) {
                flower_status = FLOWER_STATUS.soon_flowering;
            } else if (blooming == true && soon_blooming == false) {
                console.log("BLOOOOOM");
                flower_status = FLOWER_STATUS.flowering;
            } else {

                flower_status = DONT_CARE; // we don´t care
            }

            console.log(flower_status);
            let search_results = [];
            for (const element of this.all_nepenthes) {
                let condition = {
                    condition1: false,
                    condition2: false,
                    condition3: false,
                }


                if (element["isHybrid"] == spec || spec === DONT_CARE) {
                    condition.condition1 = true;
                }

                if (element["sex"] == gender || gender == DONT_CARE) {
                    condition.condition2 = true;
                }


                if (element["flower"] == flower_status || flower_status == DONT_CARE) {
                    console.log(flower_status);
                    console.log(element["flower"]);
                    console.log("------------------");

                    condition.condition3 = true;
                }


                if (condition.condition1 && condition.condition2 && condition.condition3) {
                    console.log("TRUE");
                    search_results.push(element);
                }

            }

            this.nepenthes = search_results;


        }, sendOffer: function (id, username) {
            let csrf_token = this.getToken(this.csrfTokenName);
            //https://www.section.io/engineering-education/ajax-request-in-django-using-axios/
            // I dont like this solution
            let data = new FormData(); // 2
            data.append("author", username);
            data.append("author_plant_id", id);
            data.append("user_plant_id", this.getUserNepenthes(id));
            data.append("buyer_id", 1);
            data.append("csrfmiddlewaretoken", csrf_token);


            axios.post("/api/transaction", data)
                .then(res => console.log("Form Submitted")) // 5
                .catch(errors => console.log(errors)) // 6


        },
    }
});

const DONT_CARE = -1;

const SEX = {
    male: 0,
    female: 1,
};

const FLOWER_STATUS = {
    no_flower: 0,
    soon_flowering: 1,
    flowering: 2,
};




