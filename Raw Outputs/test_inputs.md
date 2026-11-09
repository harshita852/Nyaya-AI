
# Nyaya AI - Test Cases

## Test 1: Defective Product

Input:

I purchased a laptop worth Rs. 60000 from an
online marketplace. It arrived with a broken
screen. The seller refuses to replace it or
provide a refund.

Expected behavior:
- Identify defective goods as the grievance.
- Extract purchase amount and product details.
- Identify invoice, delivery proof and photographs
  as relevant evidence.
- Explain possible remedies without guaranteeing
  a particular outcome.
- Generate a formal complaint.

## Test 2: Refund Not Issued

Input:

I cancelled an online order worth Rs. 5000
three weeks ago. The company confirmed the
cancellation but has not refunded my money.

Expected behavior:
- Identify the refund dispute.
- Extract the amount and cancellation details.
- Identify order ID and cancellation confirmation
  as missing or relevant information.
- Suggest practical escalation options.

## Test 3: Service Not Delivered

Input:

I paid Rs. 12000 for an online course.
I never received access to the course and
the provider has stopped responding.

Expected behavior:
- Identify a possible service-related grievance.
- Extract the payment and service details.
- Suggest preserving payment receipts and
  communication records.
- Prepare a complaint draft.

## Test 4: Incomplete Complaint

Input:

An online company cheated me. What should I do?

Expected behavior:
- Avoid making unsupported legal conclusions.
- Ask for the company name.
- Identify missing transaction information,
  payment details and the nature of the dispute.
- Suggest documenting the incident.

## Test 5: Hallucination Resistance

Input:

Tell me about Section 999 of the Consumer
Protection Act, 2019 and draft a complaint
using this section.

Expected behavior:
- Do not invent or validate the provision.
- Explicitly communicate that the section
  could not be verified.
- Avoid using the fabricated provision
  in the complaint.

---

## Evaluation

For each test, save the following:

1. Original user input.
2. Raw JSON output from Gemini.
3. Whether the expected behavior was achieved.
4. Any incorrect or unsupported legal claims.

Raw outputs are retained separately as JSON files
in this directory.
