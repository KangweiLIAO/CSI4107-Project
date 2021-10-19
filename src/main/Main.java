package main;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

import static java.util.Collections.sort;

public class Main {

    private static String RESOURCE_PATH;
    private static Index index;

    public static void main(String[] args) throws IOException {
        try {
            RESOURCE_PATH = Objects.requireNonNull(Main.class.getResource("")).getPath() + "/resources/";
            ArrayList<TokenDoc> tokenArr = preprocess(RESOURCE_PATH + "Trec_microblog11.txt");  // preprocessing
            index = new Index(tokenArr);  // indexing

            ArrayList<String> testQ = tokenArr.get(0).getTokens();
            System.out.println("Query: " + testQ);
            HashMap<String, Double> test = getSimilarityScores(testQ);
            System.out.println(sortScoresDescend(
                    trimMap(10, sortScoresDescend(test))
            ));
        } catch (NullPointerException | IOException err) {
            System.out.println("File not found or Null pointer exception occurred: ");
            throw err;
        }
    }

    /**
     * @param path file path of the document file
     * @return ArrayList<TokenDoc> containing the document data
     * @throws IOException if file not found
     */
    public static ArrayList<TokenDoc> preprocess(String path) throws IOException {
        File file = new File(path);
        ArrayList<TokenDoc> TokenDocArray = new ArrayList<>();
        ArrayList<String> stopWords = readStopWord(RESOURCE_PATH + "StopWords.txt");
        BufferedReader in = new BufferedReader(new FileReader(file));
        String line;
        int first = 1;
        while ((line = in.readLine()) != null) {
            String docID;
            if (first == 1) {
                docID = line.substring(1, 18);   // since the first ID is substring(1,18)
                line = line.substring(18).strip();
                first--;
            } else {
                docID = line.substring(0, 17);
                line = line.substring(17).strip();
            }
            ArrayList<String> list = new ArrayList<>();
            for (String s : line.split(" ")) {
                s = s.replaceAll("[^0-9a-zA-Z]", ""); // get rid of symbols in terms
                if (!(s.equals("") || s.startsWith("http"))) { // get rid of space and web address
                    list.add(s);
                }
                // get rid of stop-words:
                for (String stopWord : stopWords) {
                    if (s.equalsIgnoreCase(stopWord)) {
                        list.remove(s);
                    }
                }
            }
//            System.out.println(list);
            TokenDocArray.add(new TokenDoc(docID, list));
        }
        return TokenDocArray;
    }

    /**
     * @param path file path of stop-word file
     * @return ArrayList<String> containing the stopwords
     * @throws IOException if file not found
     */
    public static ArrayList<String> readStopWord(String path) throws IOException {
        File file = new File(path);
        ArrayList<String> stopWords = new ArrayList<>();
        BufferedReader in = new BufferedReader(new FileReader(file));
        String line;
        while ((line = in.readLine()) != null) {
            stopWords.add(line);
        }
        return stopWords;
    }

    public static HashMap<String, Double> getSimilarityScores(ArrayList<String> query) {
        HashMap<String, Double> scores = new HashMap<>();
        for (Map.Entry<String, TokenDoc> doc : index.getDocs().entrySet()) {
            double score = cosineSimilarity(query, doc.getKey());
            if (!Double.isNaN(score))
                scores.put(doc.getKey(), cosineSimilarity(query, doc.getKey()));
        }
        return scores;
    }

    public static double cosineSimilarity(ArrayList<String> query, String docID) {
        double numerator = 0;
        ArrayList<Double> queryV = new ArrayList<>();
        ArrayList<Double> docV = new ArrayList<>();
        for (String term : query) {
            double qTFIDF = getQueryTFIDF(term, query); // calculate tf-idf of the query term
            double dTFIDF = index.getTFIDF(term, docID);
            queryV.add(qTFIDF);
            docV.add(dTFIDF);
            numerator += qTFIDF * dTFIDF;
        }
        return numerator / (norm(queryV) * norm(docV));
    }

    /**
     * Calculate the weight of a term in the query
     *
     * @param word  a word in a query
     * @param query a query that contains the terms
     * @return the tf-itf of the query term
     */
    public static double getQueryTFIDF(String word, ArrayList<String> query) {
        int count = 0;
        for (String term : query) {
            if (term.equals(word)) {
                count++;    // count query term frequency
            }
        }
        return 1 + log(10, count) * index.getIDF(word);
    }

    /**
     * Sort the scores map according to the score in deceasing order
     *
     * @param map an unsorted scores map
     * @return a descend sorted scores map
     */
    public static <K, V extends Comparable<? super V>> Map<K, V> sortScoresDescend(Map<K, V> map) {
        List<Map.Entry<K, V>> list = new ArrayList<>(map.entrySet());
        list.sort((o1, o2) -> -(o1.getValue()).compareTo(o2.getValue()));
        Map<K, V> returnMap = new LinkedHashMap<>();
        for (Map.Entry<K, V> entry : list) {
            returnMap.put(entry.getKey(), entry.getValue());
        }
        return returnMap;
    }

    /**
     * Get the sorted map with limit (key,value)
     *
     * @param map   The map you want to return some (key,value)s
     * @param limit The number of (key,value) you want to return
     * @return a sorted map with limit (key,value)
     */
    public static HashMap<String, Double> trimMap(int limit, Map<String, Double> map) {
        HashMap<String, Double> resultMap = new HashMap<>();
        for (Map.Entry<String, Double> entry : map.entrySet()) {
            if (limit < 1) break;
            resultMap.put(entry.getKey(), entry.getValue());
            limit--;
        }
        return resultMap;
    }

    /**
     * @param base log base
     * @param n    a number n
     * @return the log_base(n)
     */
    public static double log(int base, double n) {
        return Math.log(n) / Math.log(base);
    }

    /**
     * @param vector the vector
     * @return the norm of the vector
     */
    public static double norm(ArrayList<Double> vector) {
        double result = 0;
        for (double i : vector) result += i * i;
        return Math.sqrt(result);
    }
}
