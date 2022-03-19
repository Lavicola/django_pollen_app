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
    el: '#table',
    delimiters: ['{[', ']}'],
    data: {
        csrfTokenName: "csrftoken",
        nepenthes: [],
        file_element: "",
        dropdown_sex_element: "dropdown_sex_",
        dropdown_shipping_element: "dropdown_shipping_",
        dropdown_flower_element: "dropdown_flower_",
        name_element: "name_",
        description_element: "description_",
        file_element: "file_",
    },
    mounted: function () {
        this.getNepenthes();

        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        axios.defaults.xsrfCookieName = "csrftoken";
        axios.defaults.withCredentials = true;

    },
    methods: {
        getToken: function (name) {
            // https://stackoverflow.com/a/15724300
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        },
        getNepenthes: function () {
            let api_base_url = '/api/nepenthes/edit/';
            axios.get(api_base_url)
                .then((response) => {
                    this.nepenthes = response.data;
                }).catch(error => {
                console.log(error);
            })
        },
        updateNepenthes: function (id){

            let name = document.getElementById(this.name_element+id).innerText;
            let description = document.getElementById(this.description_element+id).innerText;
            let sex = document.getElementById(this.dropdown_sex_element+id).value;
            let shipping = document.getElementById(this.dropdown_shipping_element+id).value;
            let flower = document.getElementById(this.dropdown_flower_element+id).value;
            let file = document.getElementById(this.file_element+id).files[0];


            console.log(file);

            let formData = new FormData();
            let csrf_token = this.getToken(this.csrfTokenName);

            formData.append("plant_id", id);
            formData.append("name", name);
            formData.append("description", description);
            formData.append("sex",sex);
            formData.append("shipping", shipping);
            formData.append("flower", flower);
            formData.append("image", file);
            formData.append("csrfmiddlewaretoken", csrf_token);




        axios.put("/api/nepenthes/edit/", formData)
            .then(res => {
                    if (res.status == 201) {
                        return;
                    } else {
                        alert("something went wrong");
                    }
                }
            ) // 5
            .catch(errors => console.log(errors)) // 6

            // todo use put/patch instead post
            axios.post('/api/nepenthes/edit/', formData, {
                headers: {
                  'Content-Type': 'multipart/form-data'
                }});




        },
        removeNepenthes: function (index){
            // TODO delete request
            this.$delete(this.nepenthes,index);
            },


}});




