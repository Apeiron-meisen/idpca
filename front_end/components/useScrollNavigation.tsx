import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
const useScrollNavigation = () => {
  const router = useRouter();
  const page_list = ['/','/page_2','/page_3','/page_4','/page_5']
  
  useEffect(() => {
    const handleScroll = (event: WheelEvent) => {
      const currentPath = window.location.pathname;
      const currentIndex = page_list.indexOf(currentPath);
      if (event.deltaY > 0) {
        const new_index:number = (currentIndex + 1) % 5
        console.log("current_index:! " + new_index)
        // Change to your next page route
        router.push(page_list[new_index]); // Change to your next page route
      } else if (event.deltaY < 0) {
        const new_index:number = (currentIndex - 1) % 5
        router.push(page_list[(new_index)]); // Change to your previous page route
      }
    };

    window.addEventListener('wheel', handleScroll);
    // ?
    return () => window.removeEventListener('wheel', handleScroll);
  }, [router]);
}

export default useScrollNavigation;
