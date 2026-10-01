import re

with open(r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\scripts\auto_crawler.py', 'r', encoding='utf-8') as f:
    code = f.read()

# We want to replace the block starting at 'except Exception as e1:' and ending before '# --- END WATERFALL ---'
start_idx = code.find('            except Exception as e1:')
end_idx = code.find('            # --- END WATERFALL ---', start_idx)

correct_block = '''            except Exception as e1:
                print(f"⚠️ Groq API failed (Limit Reached).")
                
                print("🧠 Groq failed. Falling back to Gemini Backup AI...")
                gemini_success = False
                if gemini_cycle is not None and len(gemini_clients) > 0:
                    # Loop through all available Gemini keys to find one that isn't rate-limited
                    for _ in range(len(gemini_clients)):
                        current_gemini = next(gemini_cycle)
                        try:
                            response = current_gemini.models.generate_content(
                                model='gemini-3.5-flash',
                                contents=prompt,
                                config=types.GenerateContentConfig(
                                    response_mime_type="application/json",
                                    response_schema=MaterialSchema,
                                    temperature=0.1
                                ),
                            )
                            material_data = json.loads(response.text)
                            material_data["extraction_method"] = "Gemini"
                            gemini_success = True
                            break  # Success! Break out of the Gemini key loop
                        except Exception as gemini_err:
                            # This specific key failed (likely rate limit), continue to the next one
                            pass
                
                if not gemini_success:
                    print(f"⚠️ All {len(gemini_clients)} Gemini APIs failed (Limits Reached).")
                    try:
                        print("🧠 Gemini failed. Falling back to OpenAI (gpt-4o-mini)...")
                        response = openai_client.chat.completions.create(
                            model="gpt-4o-mini",
                            response_format={"type": "json_object"},
                            messages=[
                                {"role": "system", "content": f"You are a data extractor. Output ONLY valid JSON matching this exact schema: {MaterialSchema.model_json_schema()}"},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.1
                        )
                        material_data = json.loads(response.choices[0].message.content)
                        material_data["extraction_method"] = "OpenAI"

                    except Exception as e3:
                        print(f"⚠️ OpenAI API failed (Limit Reached).")
                        if "makeitfrom.com" in page_url or "aalco.co.uk" in page_url:
                            material_data = fallback_scraper(raw_markdown, page_url)
                            material_data["extraction_method"] = "Deterministic Parser"
                        else:
                            print("❌ All AIs failed, and deterministic fallback cannot read random sources.")'''

if start_idx != -1 and end_idx != -1:
    new_code = code[:start_idx] + correct_block + '\n' + code[end_idx:]
    with open(r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\scripts\auto_crawler.py', 'w', encoding='utf-8') as f:
        f.write(new_code)
    print("Fixed Gemini rotation block!")
else:
    print("Could not find blocks to replace!")
