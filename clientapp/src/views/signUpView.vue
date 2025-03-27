<template>

  <form class="row g-3">
    <div class="col-12">
      <label for="inputEmail4" class="form-label">Email</label>
      <input type="email" class="form-control" id="inputEmail4">
    </div>
    <div class="col-md-6">
      <label for="username" class="form-label">Username</label>
      <input type="username" class="form-control" id="username">
    </div>
    <div class="col-md-6">
      <label for="inputPassword4" class="form-label">Password</label>
      <input type="password" class="form-control" id="inputPassword4">
    </div>
    <div v-if="!businessCheck" class="col-md-6">
      <label for="inputFirstName" class="form-label">First Name</label>
      <input type="firstName" class="form-control" id="inputFirstName">
    </div>
    <div v-if="!businessCheck" class="col-md-6">
      <label for="inputLastName" class="form-label">Last Name</label>
      <input type="lastName" class="form-control" id="inputLastName">
    </div>
    <div v-if="businessCheck" class="col-12">
      <label for="inputCompanyName" class="form-label">Company Name</label>
      <input type="text" class="form-control" id="inputCompanyName" v-model="inputCompanyName">
    </div>
    <div class="col-12">
      <label for="inputAddress" class="form-label">Address</label>
      <input type="text" class="form-control" id="inputAddress" placeholder="1234 Main St">
    </div>
    <div class="col-12">
      <label for="inputAddress2" class="form-label">Address 2</label>
      <input type="text" class="form-control" id="inputAddress2" placeholder="Apartment, studio, or floor">
    </div>
    <div class="col-md-4">
      <label for="inputCity" class="form-label">City</label>
      <input type="text" class="form-control" id="inputCity">
    </div>
    <div class="col-md-4">
      <label for="inputState" class="form-label">State</label>
      <select id="inputState" class="form-select">
        <option selected>Choose...</option>
        <option>...</option>
      </select>
    </div>
    <div class="col-md-2">
      <label for="inputZip" class="form-label">Zip</label>
      <input type="text" class="form-control" id="inputZip">
    </div>
    <div class="col-md-2">
      <label for="inputPhone" class="form-label">Phone Number</label>
      <input type="text" class="form-control" id="inputPhone">
    </div>
    <div class="col-md-6">
      <div class="form-check">
        <input class="form-check-input" type="checkbox" id="termsCheck">
        <label class="form-check-label" for="termsCheck">
          Review and accept the <a href="/termsandconditions" target="_blank">terms and conditions</a> 
        </label>
      </div>
    </div>
    <div class="col-md-6">
      <div class="form-check">
        <input class="form-check-input" type="checkbox" v-model="businessCheck">
        <label class="form-check-label" for="businessCheck">
          Business Account
        </label>
      </div>
    </div>
    <div class="col-12">
      <button type="submit" class="btn btn-primary">Register</button>
    </div>
  </form>

  <p v-if="message" :class="messageClass">{{ message }}</p>

</template>


<script>
import authService from '../services/authService';

 export default {
  data() {
    return {
      businessCheck: false,  // TypeScript type declaration
      inputCompanyName: '',
    };
  },

 methods: {
  submitForm() {
    const data = {
      email: this.email,
      company_name: this.inputCompanyName,
      username: this.username,
      firstname: this.firstname,
      lastname: this.lastname,
      password: this.password,
      terms: this.terms,
      address: this.address,
      city: this.city,
      state: this.state,
      zip: this.zip,
      phone: this.phone,
      is_business: this.is_business,
      is_admin: false
    };
    
    authService.register(data)
    .then(() => {
          this.message = 'Registration successful!';
          this.messageClass = 'success';
          this.name = ''; // Clear the input field
        })
        .catch(() => {
          this.message = 'Error registering name';
          this.messageClass = 'error';
        });
    }
  }
};

 </script>

  

<style scoped>
.form-check {
  display: flex;
  align-items: center; /* Align the checkbox and label vertically */
  justify-content: center;
}

.form-check-input {
  margin-right: 5px; /* Reduce the space between the checkbox and label */
  align-items: center;
}
</style>