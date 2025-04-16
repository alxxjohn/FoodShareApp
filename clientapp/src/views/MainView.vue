<script setup>
 import { useRouter } from 'vue-router';
 import { onMounted } from 'vue';

 const router = useRouter();
 
onMounted(async () => {
  
  const is_business = localStorage.getItem('is_business');
  if(is_business){
    router.push('/reservation-lis');
  } else {
    router.push('/foodmap');
  }
});


</script>
