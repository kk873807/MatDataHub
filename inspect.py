import os

path = r'c:\Users\KISHAN\Documents\Matdata\MatDataHub\next-frontend\src\app\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the missing closing divs
text = text.replace('            </div>\n\n          </div>\n        </div>\n      </section>', '            </div>\n\n          </div>\n        </div>\n      </section>')
text = text.replace('          </div>\n        </div>\n      </section>', '          </div>\n      </section>') # wait

# Let's just fix it properly by searching for `          </div>\n        </div>\n      </section>`
# Actually let's just rewrite the end of the block.
old_str = """              <Link href="/account" className="block text-center w-full py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold transition-colors">Get Advanced</Link>
            </div>

          </div>
        </div>
      </section>"""

new_str = """              <Link href="/account" className="block text-center w-full py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold transition-colors">Get Advanced</Link>
            </div>

          </div>
        </div>
      </section>"""

# Wait, if `</div>\n        </div>` is already there, why did it complain?
# Let's look at the actual source of `src/app/page.tsx` line 265 to 275.
