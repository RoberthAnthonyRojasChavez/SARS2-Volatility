package correlation;

import java.util.function.Predicate;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import dataStructures.Entry;
import exceptions.ListSizeMisMatchException;
import static ch.obermuhlner.math.big.BigDecimalMath.factorial;

import java.util.List;

/**
 * Compute p-value of Fisher's Exact Test
 *
 * Created by rdong6 on 6/22/2018.
 */
public class FisherExact<T> implements Correlation<T> {

    private static final int SIG_FIGS = 100; // significant figures for intermediate calculations
    private final Predicate<T> predicate;

    public FisherExact (Predicate<T> predicate) {
        this.predicate = predicate;
    }

    public double calcPValue(List<T> list1, List<T> list2) throws ListSizeMisMatchException {

        if (list1.size() != list2.size())
            throw new ListSizeMisMatchException();

        // set up the four quadrants needed for calculations
        ArrayList<Entry<Boolean, Boolean>> entries = new ArrayList<>();
        for (int i = 0; i < list1.size(); i++)
            entries.add(new Entry<>(predicate.test(list1.get(i)), predicate.test(list2.get(i))));
        int q1 = 0, q2 = 0, q3 = 0, q4 = 0;
        for (Entry<Boolean, Boolean> entry : entries) { // previous List of Boolean pairs
            if (!entry.getKey() && !entry.getValue())
                q4 += 1;
            else if (!entry.getKey())
                q1 += 1;
            else if (!entry.getValue())
                q3 += 1;
            else
                q2 += 1;
        }

        // calculate p value for fisher exact
        return nCr(q2 + q1, q2)
                .multiply(nCr(q3 + q4, q3))
                .divide(nCr(q1 + q2 + q3 + q4, q2 + q3), RoundingMode.CEILING)
                .doubleValue();
    }

    private static BigDecimal nCr(int n, int r) {
        BigDecimal result = factorial(n).divide(factorial(r).multiply(factorial(n - r)), RoundingMode.HALF_EVEN);
        // limit to 10-significant figures
        int newScale = SIG_FIGS - result.precision() + result.scale();
        result = result.setScale(newScale, RoundingMode.HALF_EVEN);
        return result;
    }
}
