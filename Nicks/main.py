    public static int randomNumber(int length) {
        StringBuilder builder = new StringBuilder();
        char[] numbers = "1234567890".toCharArray();
        while (builder.length() != length) {
            for (int i = 0; i < length; i++) {
                builder.append(numbers[random.nextInt(numbers.length)]);
            }
        }
        // пример: 98481 (length = 5)
        return Integer.parseInt(builder.toString());
    }
    public static String randomString(int length) {
        StringBuilder builder = new StringBuilder();
        char[] letters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM".toCharArray();
        while (builder.length() != length) {
            for (int i = 0; i < length; i++) {
                if (random.nextBoolean()) builder.append(letters[random.nextInt(letters.length)]);
                else builder.append(Character.toUpperCase(letters[random.nextInt(letters.length)]));
            }
        }
        // пример: glCsk (length = 5)
        return builder.toString();
    }
