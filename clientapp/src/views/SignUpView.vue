<template>

  <form @submit.prevent="submitForm" class="">
    <div class="row py-4">
      <div class="col-md-6">
        <label for="username" class="form-label">Username</label>
        <input type="username" class="form-control" id="username" v-model="username">
      </div>
      <div class="col-md-6">
        <label for="inputPassword4" class="form-label">Password</label>
        <input type="password" class="form-control" id="inputPassword4" v-model="password">
      </div>
    </div>
    <div class="row py-4">
      <div class="col-md-6">
        <label for="inputEmail4" class="form-label">Email</label>
        <input type="email" class="form-control" id="inputEmail4" v-model="email">
      </div>
      <div v-if="accountTypeRadio === 'personal'" class="col-md-3">
        <label for="inputFirstName" class="form-label">First Name</label>
        <input type="firstName" class="form-control" id="inputFirstName" v-model="firstname">
        </div>
      <div v-if="accountTypeRadio === 'personal'" class="col-md-3">
        <label for="inputLastName" class="form-label">Last Name</label>
        <input type="lastName" class="form-control" id="inputLastName" v-model="lastname">
      </div>
      <div v-if="accountTypeRadio !== 'personal'" class="col-md-6">
        <label for="inputCompanyName" class="form-label">Company Name</label>
        <input type="text" class="form-control" id="inputCompanyName" v-model="company_name">
      </div>
    </div>

    <div class="row py-4">
      <div class="col-md-6">
        <label for="inputAddress" class="form-label">Address</label>
        <input type="text" class="form-control" id="inputAddress" placeholder="1234 Main St" v-model="address">
      </div>
      <div class="col-md-6">
        <label for="inputAddress2" class="form-label">Address 2</label>
        <input type="text" class="form-control" id="inputAddress2" placeholder="Apartment, studio, or floor" v-model="address2">
      </div>
    </div>

    <div class="row py-4">
      <div class="col-md-3">
        <label for="inputCity" class="form-label">City</label>
        <input type="text" class="form-control" id="inputCity" v-model="city">
      </div>
    
      <div class="col-md-3">
        <label for="inputState" class="form-label">State</label>
        <select id="inputState" class="form-select" v-model="selectedState">
          <option v-for="state in states" :key="state" :value="state">
            {{ state }}
          </option>
        </select>
      </div>

      <div class="col-md-3">
        <label for="inputZip" class="form-label">Zip</label>
        <input type="text" class="form-control" id="inputZip" v-model="zip">
      </div>
      <div class="col-md-3">
        <label for="inputPhone" class="form-label">Phone Number</label>
        <input type="text" class="form-control" id="inputPhone" v-model="phone">
      </div>
    </div>

    <div class="row d-flex align-items-center py-4">
      <div class="col-md-6">
        <div class="form-check">
          <input class="form-check-input" type="checkbox" id="termsCheck">
          <label class="form-check-label" for="termsCheck">
            Review and accept the <a href="/termsandconditions" target="_blank">terms and conditions</a> 
          </label>
        </div>
      </div>
      <div class="col-md-6">
        <div class="radio-container">
          <p>Select an account type</p>
          <label class="radio-label">
            <input class="form-check-input" type="radio" v-model="accountTypeRadio" value="personal" @change="is_business = false"> Personal
          </label>
          <label class="radio-label">
            <input class="form-check-input" type="radio" v-model="accountTypeRadio" value="business" @change="is_business = true"> Business
          </label>
          <label class="radio-label">
            <input class="form-check-input" type="radio" v-model="accountTypeRadio" value="foodbank" @change="is_foodbank = true"> Food Bank
          </label>
        </div>
      </div>
    </div>


    <div class="d-flex justify-content-center">
      <button type="submit" class="btn btn-primary">Register</button>
    </div>
  </form>

  <p v-if="submitted" :class="messageClass">{{ message }}</p>

</template>


<script>
import authService from '@/services/authService';
import { states } from '@/utils/const.js';


 export default {
  
  data() {
    return {
      email: '',
      accountTypeRadio: 'personal',  // TypeScript type declaration
      username: '',
      firstname: '',
      lastname: '',
      password: '',
      states: states,
      selectedState: '',
      terms: false,
      address: '',
      address2: '',
      city: '',
      zip: '',
      phone: '',
      submitted: false,
      is_business:false,
      is_foodbank:false,
      is_admin:false,
      company_name: ''
    };
    
    
  },

  methods: {
  
  submitForm() {
    const requestTemplate = {
      email: this.email,
      username: this.username,
      firstname: this.firstname,
      lastname: this.lastname,
      password: this.password,
      address: this.address,
      city: this.city,
      state: this.selectedState,
      zipCode: this.zip,
      phone: this.phone,
      is_business: this.is_business,
      is_admin: this.is_admin 
    };

    const userRequest = {
      ...requestTemplate,
      terms: true
    }

    const businessRequest = {
      ...requestTemplate,
      is_foodbank: this.is_foodbank,
      tos_accepted: true,
      company_name: this.company_name
    };

    if(!this.is_business){
      console.log("userRequest: " + JSON.stringify(userRequest));
      
      authService.userRegister(userRequest)
      .then((response) => {
        console.log(response)
        this.$router.push('/login');
        })
      .catch((error) => {
        console.log(error.response);
        this.message = 'Error registering name';
        this.messageClass = 'error';
      });
    } else {
      console.log("businessRequest: " + JSON.stringify(businessRequest));
      
      authService.businessRegister(businessRequest)
      .then((response) => {
        console.log(response)
        this.$router.push('/login');
        })
      .catch((error) => {
        console.log(error.response);
        this.message = 'Error registering name';
        this.messageClass = 'error';
      });
    }}
  },
}
 </script>

  

<style scoped>
.form-check {
  display: flex;
  align-items: center; /* Align the checkbox and label vertically */
  justify-content: center;
}

input[type="radio"] {
      margin-left: 20px; /* Add spacing between radio buttons */
    }

.form-check-input {
  margin-right: 5px; /* Reduce the space between the checkbox and label */
  align-items: center;
}
</style>