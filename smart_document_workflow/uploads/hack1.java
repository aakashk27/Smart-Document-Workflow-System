import java.util.*;
public class hack1 {
    public static List<Integer> op(List<String> lists) {
        List<Integer> c = new ArrayList<>();
        
        for (String words : lists) {
            char[] charArray = words.toCharArray();
            int count = 0;
            int i = 0;
            while (i < charArray.length - 1) {
                if (charArray[i] == charArray[i + 1]) {
                    count++;
                    i++;
                }
                i++;
            }
            c.add(count);
        }
        
        return c;
    }

    public static void main(String[] args) {
        List<String> lists = new ArrayList<>();
     lists.add("boook");
     lists.add("add");
     lists.add("break");
         List<Integer> result = op (lists);
        System.out.println(result);}
}
