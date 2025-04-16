<script setup>
 import authService from '@/services/authService';
 import { useRouter } from 'vue-router';

 const router = useRouter();
 
onMounted(async () => {
  try {
    const userInfo = await authService.getCurrentLoggedInUser();

    if(userInfo.data.is_business){
      router.push('/reservation-lis');
    } else {
      router.push('/foodmap');
    }

  } catch (error) {
    console.log("Unable to retrieve the current user", error);
  }
});


</script>
