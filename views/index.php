<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Form</title>
    <link rel="stylesheet" href="../assets/css/style.css" />
  </head>

  <body>
    <form action="../backend/save_receipt.php" method="post" autocomplete="off">
      <p class="title">RECEIPT DATA</p>

      <label style="display: flex">
        <span>Name : </span>
        <input type="text" name="name" placeholder="Donor's Name" required />
      </label>
      <input type="date" name="date" value="2025-10-12" required />

      <label>
        <span>Amount : </span>
        <input
          type="number"
          name="amount"
          placeholder="Donation"
          min="0"
          required
        />
      </label>

      <label class="radio">
  <span>Payment Type : </span>
  <input type="radio" name="paytype" value="cash" checked /><span>cash</span>
  <input type="radio" name="paytype" value="gpay" /><span>gpay</span>
  <input type="radio" name="paytype" value="cheque" /><span>cheque</span>
</label>

<!-- Reference / Cheque Number (hidden initially) -->
<label id="ref_label" style="display:none;">
  <span id="ref_span">Reference Number: </span>
  <input type="text" name="ref_no" id="ref_no" placeholder="Enter reference number" />
</label>

<script>
  const radios = document.querySelectorAll('input[name="paytype"]');
  const refLabel = document.getElementById('ref_label');
  const refSpan = document.getElementById('ref_span');

  radios.forEach(radio => {
    radio.addEventListener('change', () => {
      if(radio.value === 'gpay') {
        refLabel.style.display = 'flex';
        refSpan.textContent = 'Reference Number:';
      } else if(radio.value === 'cheque') {
        refLabel.style.display = 'flex';
        refSpan.textContent = 'Cheque Number:';
      } else {
        refLabel.style.display = 'none';
      }
    });
  });
</script>


      <label>
        <span>Category : </span>
        <select name="category_id" required>
         <?php
         include "../backend/db.php"; // make sure path is correct

         $result = $conn->query("SELECT Category_ID, Category FROM donation_category WHERE Active=1");
         while ($row = $result->fetch_assoc()) {
             echo '<option value="'.$row['Category_ID'].'">'.htmlspecialchars($row['Category']).'</option>';
          }
          ?>
        </select>
      </label>
      <br />

      <button type="submit" name="submit">submit</button>
    </form>
  </body>
</html>


