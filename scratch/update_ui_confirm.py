import sys
import re

with open('next-frontend/src/app/analytics/cbam/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# I need to add state for the confirmation modal
state_injection = """  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [confirmData, setConfirmData] = useState({ rows: 0, weight: 0 });"""

content = re.sub(r'(const \[error, setError\] = useState<string \| null>\(null\);)', r'\1\n' + state_injection, content)

# Modify onSubmit
old_submit = """  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file && !pastedText) return;

    setLoading(true);
    setError(null);
    setResultsData([]);"""

new_submit = """  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file && !pastedText) return;

    // Parse file/text first to confirm
    let textToParse = pastedText;
    if (file) {
      textToParse = await file.text();
    }
    
    Papa.parse(textToParse, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        let totalWeight = 0;
        let weightCol = "";
        
        if (results.data.length > 0) {
          const keys = Object.keys(results.data[0] as any);
          weightCol = keys.find(k => k.toLowerCase().includes('weight') || k.toLowerCase().includes('qty') || k.toLowerCase().includes('quantity') || k.toLowerCase().includes('mass')) || "";
        }
        
        if (weightCol) {
          totalWeight = results.data.reduce((acc, row: any) => {
             const val = row[weightCol];
             if (!val) return acc;
             // handle European and US
             let cleanVal = String(val).replace(/ /g, '');
             if (cleanVal.match(/^\d{1,3}(?:\.\d{3})*,\d+$/)) {
                cleanVal = cleanVal.replace(/\./g, '').replace(',', '.');
             } else if (cleanVal.match(/^\d+,\d+$/)) {
                cleanVal = cleanVal.replace(',', '.');
             } else {
                cleanVal = cleanVal.replace(/,/g, '');
             }
             return acc + (parseFloat(cleanVal) || 0);
          }, 0);
        }
        
        setConfirmData({ rows: results.data.length, weight: totalWeight / 1000 }); // convert kg to t
        setShowConfirmModal(true);
      }
    });
  };

  const handleConfirmedSubmit = async () => {
    setShowConfirmModal(false);
    setLoading(true);
    setError(null);
    setResultsData([]);"""

content = content.replace(old_submit, new_submit)

# Close handleConfirmedSubmit
old_fetch_end = """        setError(err instanceof Error ? err.message : "Failed to analyze BOM.");
      }
    } catch (err: any) {
      setError(err.message || "Failed to analyze BOM.");
    } finally {
      setLoading(false);
    }
  };"""

new_fetch_end = """        setError(err instanceof Error ? err.message : "Failed to analyze BOM.");
      }
    } catch (err: any) {
      setError(err.message || "Failed to analyze BOM.");
    } finally {
      setLoading(false);
    }
  };"""

# Wait, `handleConfirmedSubmit` closes exactly where `onSubmit` used to close!
# We just rename the end of `onSubmit`? No, the function signature was changed.
# Let's replace the whole onSubmit.

# Wait, replacing the whole onSubmit via regex might be safer.
