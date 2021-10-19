package main;
import java.util.*;

/**
 * @author Kangwei Liao
 * <p>
 * Represents inverted indexing, stored using hashmap.
 */
public class Index {

    private final int numOfDocs;
    private final HashMap<String, LinkedList<Map.Entry<String, Double>>> termMap; // HashMap<term, LinkedList<Map.Entry<docID, weight>>>
    private final HashMap<String, Integer> freqMap; // HashMap<term, frequency>
    private final HashMap<String, TokenDoc> docMap; // HashMap<term, docSize>

    /**
     * Constructor of Index class, base on the input documents output an inverted index map
     *
     * @param docs a list of {TokenDoc} instance to initialize an inverted index instance
     */
    public Index(ArrayList<TokenDoc> docs) {
        numOfDocs = docs.size();
        termMap = new HashMap<>();
        freqMap = new HashMap<>();
        docMap = new HashMap<>();
        var nnn = 100;
        for (TokenDoc doc : docs) {
            docMap.put(doc.getID(), doc);
            ArrayList<String> tokens = doc.getTokens(); // get tokens from tokenized document
            Set<String> uniqueSet = new LinkedHashSet<>();
            for (String token : tokens) {
                if (nnn > 0) {
                    System.out.println(token);
                    nnn--;
                }
                uniqueSet.add(token);
                token = token.toLowerCase();
                Map.Entry<String, Double> tmp = new AbstractMap.SimpleEntry<>(doc.getID(), getTF(token, doc.getID())); // (docID, TF) pair for a term
                if (termExist(token)) { // if token in index, append the (docID,tfValue) to the corresponding term
                    termMap.get(token).add(tmp);
                } else { // if token not in index, put the term into the hashmap
                    termMap.put(token, new LinkedList<>(List.of(tmp)));
                }
                if (freqMap.get(token) == null) {
                    freqMap.put(token, 1);
                } else if (!uniqueSet.contains(token)) {
                    uniqueSet.add(token); // used to prevent duplicated terms counted in freq in one doc
                    freqMap.replace(token, freqMap.get(token) + 1); // update freqMap for the term
                }
            }
        }
    }

    /**
     * @param term  a word
     * @param docID a docID
     * @return the TF weight of this word in this document
     */
    private double getTF(String term, String docID) {
        double rawTF = 0.;
        for (String words : docMap.get(docID).getTokens()) {
            if (words.equalsIgnoreCase(term)) rawTF++;
        }
        if (rawTF == 0) return 0;
        return rawTF / docMap.get(docID).getTokens().size();
    }

    /**
     * @param term a word
     * @return the idf of the word in indexing
     */
    public double getIDF(String term) {
        if (!termExist(term)) return 0;
        return 1 + Main.log(10, (double) numOfDocs / getFrequency(term));
    }

    /**
     * @param term  a word
     * @param docID a specified docID
     * @return the tf-idf of the word in docID
     */
    public double getTFIDF(String term, String docID) {
        term = term.toLowerCase();
        if (!termExist(term)) return 0;
        return getTF(term, docID) * getIDF(term);
    }

    /**
     * @param term a word
     * @return true if the term exist in inverted index, false otherwise.
     */
    public boolean termExist(String term) {
        return termMap.get(term.toLowerCase()) != null;
    }

    /**
     * Return posting in form of LinkedList[Map.Entry[docID, weight]]
     *
     * @param term a word
     * @return the posting of the word
     * @throws NullPointerException if the word is not found in inverted index map
     */
    public LinkedList<Map.Entry<String, Double>> getPosting(String term)
            throws NullPointerException {
        return termMap.get(term.toLowerCase());
    }

    /**
     * @return the total number of document in this inverted index map
     */
    public int getNumOfDocs() {
        return numOfDocs;
    }

    /**
     * @param term a word
     * @return how many times this word appears in documents
     * @throws NullPointerException if the word is not found in inverted index map
     */
    public int getFrequency(String term) throws NullPointerException {
        return freqMap.get(term.toLowerCase());
    }

    /**
     * @return return a map containing all documents in inverted index map
     */
    public HashMap<String, TokenDoc> getDocs() {
        return docMap;
    }

    /**
     * @return the length (number of terms) of the inverted index map
     */
    public int numOfTerms() {
        return termMap.size();
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder();
        for (Map.Entry<String, LinkedList<Map.Entry<String, Double>>> entry : termMap.entrySet()) {
            String term = entry.getKey();
            result.append("{").append(term).append("(").append(getFrequency(term)).append(") : ");
            for (Map.Entry<String, Double> pair : entry.getValue()) {
                result.append("[").append(pair).append("], ");
            }
            result.append("}");
        }
        return result.toString();
    }
}