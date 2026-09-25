# presentHITs Weaver Guide

## Quick Start

### Activate the @presentHITs Agent

Use any of these trigger methods:

```bash
@presentHITs

"create slides"

"make presentation"  

"build deck"
```

---

## How It Works

### 1. **The Setup**

- **You (Director)**: Provide strategic narrative, content outline, or raw data
- **@presentHITs (Architect)**: Transform your content into immersive HTML presentations

### 2. **The Workflow**

```
Your Content
    ↓
@presentHITs agent activated
    ↓
Calibration header displayed
    ↓
HTML slide deck generated
    ↓
Interactive presentation delivered
    ↓
Optional: Export to PowerPoint
```

### 3. **The Output**

- **Format**: Single-file HTML (self-contained, no dependencies)
- **Delivery**: Full-screen interactive presentation
- **Navigation**: Arrow keys (← →) or Next/Prev buttons
- **Export**: Convert to PPTX using included converter script

---

## Example Usage

### Simple Request

**You:**
```
@presentHITs

Create slides about the three stages of TechnoPhage:
- Stage I: Proof of Value (Seed)
- Stage II: Industrialization (Muscle)  
- Stage III: Systemic Innovation (Symbiont)

Include key metrics for each stage.
```

**Result**: Executive-grade presentation with 13 slides covering strategy, workflow, metrics, and investment thesis.

---

## Customization Options

### Color Themes

The default theme uses:
- **Background**: Slate-900 (dark navy)
- **Primary Accent**: Sky-400 (cyan)
- **Secondary Accent**: Emerald-400 (green)
- **Text**: Slate-100 (white)

**To customize**, modify the Tailwind color classes in the generated HTML:

```html
<!-- Change primary accent from sky-400 to rose-400 -->
<h1 class="...bg-gradient-to-r from-rose-400 to-emerald-400...">
```

Tailwind utilities available:
- Colors: `slate`, `sky`, `cyan`, `emerald`, `indigo`, `rose`, `amber`, etc.
- Opacity: `bg-opacity-20` to `bg-opacity-80`
- Contrast: Adjust `text-slate-X` (100-900)

### Layout Variants

**Title Slide** (Cover)
```html
<section class="slide active h-full w-full flex flex-col justify-center items-center p-12 text-center">
    <h1 class="text-6xl font-extrabold...">Main Title</h1>
    <p class="text-2xl text-slate-300...">Subtitle</p>
</section>
```

**Content Slide** (2-Column Grid)
```html
<div class="grid grid-cols-2 gap-8 w-full max-w-5xl">
    <div class="bg-slate-800 p-6 rounded-xl...">Point 1</div>
    <div class="bg-slate-800 p-6 rounded-xl...">Point 2</div>
</div>
```

**3-Column Grid**
```html
<div class="grid grid-cols-3 gap-6 w-full max-w-6xl">
    <!-- Three cards -->
</div>
```

**Stage Cards** (Left-bordered)
```html
<div class="stage-card stage-1">
    <h3 class="text-xl font-bold text-sky-300 mb-3">Stage Title</h3>
    <p class="text-sm text-slate-300">Content</p>
</div>
```

### Typography

- **H1** (Main titles): `text-6xl font-extrabold` + gradient text
- **H2** (Section headers): `text-4xl font-bold text-sky-400`
- **H3** (Card titles): `text-xl font-bold`
- **Body text**: `text-sm` or `text-xs` with `text-slate-300`
- **Emphasis**: `font-bold text-emerald-400`

---

## Export to PowerPoint

### Prerequisites

```bash
npm install pptx-gen-js
```

### Convert HTML to PPTX

```bash
node /path/to/html-to-pptx-converter.js technophage_presentation.html technophage.pptx
```

**Output**:
- PowerPoint file with same content structure
- Tailwind colors mapped to PPTX palette
- Slide numbers preserved
- Text and formatting maintained

### What's Converted

✓ Slide titles and subtitles  
✓ Text content and body paragraphs  
✓ List items (with bullets)  
✓ Card-based layouts  
✓ Color scheme (Slate-900 background, Cyan accents)  
✓ Slide numbering

⚠️ **Limitations**:
- Complex animations not supported (PPTX limitation)
- Tailwind hover states converted to static
- Gradient text simplified to solid colors
- Shadow effects simplified

---

## Best Practices

### Content Organization

1. **Lead with narrative**: Establish your core message first
2. **Use three-act structure**: Opening → Development → Closing
3. **One idea per slide**: Avoid cognitive overload
4. **Visual hierarchy**: Use headers, cards, and spacing strategically

### Effective Slide Types

**Opening Slide**
- Big, bold title
- Concise subtitle
- Optional: tagline or value proposition

**Data/Metrics Slide**
- KPIs in large, prominent text
- Color-coded cards (green=good, red=risk, blue=neutral)
- Grid layout for comparison

**Process/Workflow Slide**
- Flowchart with arrows (use monospace font + arrow symbols)
- Steps clearly numbered
- Visual demarcation (boxes, colors)

**Summary/Closing Slide**
- Echo the opening slide design
- Call-to-action or key takeaway
- Contact/next steps information

---

## Operational Protocols

### Calibration Header

presentHITs inherits its header from the repo-wide Output Frame standard
(`~/.agents/instructions/workspace-config/output-frame.instructions.md`),
not a bespoke block — see `SKILL.md`'s "Output Frame" section for the
exact 3-line reference:

```
Header: inherits OUTPUT-FRAME (~/.agents/instructions/workspace-config/output-frame.instructions.md).
MODE = `ARCHITECT_ANALYST`; Focus default = `Narrative Flow`.
Persona extension = archi-family (always full header + DIALECTIC).
```

As an archi-family persona, presentHITs always emits the full Output Frame
header (even on short replies) plus the DIALECTIC extension line. This
signals:
- Agent mode activated (`ARCHITECT_ANALYST`)
- Structural confidence level (`RESONANCE`)
- Design focus area (`Focus`)
- Any design trade-offs or risks (`DIALECTIC`)
- Narrative intent understood (`ANALYSIS`)
- Generation timestamp (`TIMESTAMP`)

### Quality Checklist

Before finalizing:
- ✓ Narrative arc is clear (intro → development → resolution)
- ✓ Visuals support story, not distract from it
- ✓ Color contrast passes accessibility standards
- ✓ Typography is consistent across slides
- ✓ Navigation is intuitive (keyboard + buttons work)
- ✓ Slide count is appropriate (12-15 slides for executive presentation)

---

## Troubleshooting

### Issue: Slides not displaying

**Solution**: Ensure the HTML file is opened in a modern browser. Check browser console for JavaScript errors.

### Issue: Colors not rendering correctly

**Solution**: Verify Tailwind CDN is loading (`<script src="https://cdn.tailwindcss.com"></script>`). Check for CSS conflicts.

### Issue: PPTX conversion fails

**Solution**: 
1. Verify `pptx-gen-js` is installed: `npm list pptx-gen-js`
2. Check input HTML file path is correct
3. Ensure write permissions in output directory
4. Run: `node html-to-pptx-converter.js --help` for debug info

### Issue: Presentation looks different across browsers

**Solution**: Tailvwind CSS is CDN-loaded. Offline viewing may require downloading Tailwind CSS locally and embedding it in the HTML.

---

## Advanced: Creating Reusable Templates

### Template Structure

Save commonly-used slide patterns:

**Pattern: Two-Column Comparison**
```html
<section class="slide h-full w-full flex flex-col justify-center items-center p-12">
    <h2 class="text-4xl font-bold text-sky-400 mb-10 w-full border-b border-sky-800 pb-4">Title</h2>
    <div class="grid grid-cols-2 gap-8 w-full max-w-5xl">
        <div class="bg-slate-800 p-6 rounded-xl border border-slate-700">
            <h4 class="text-cyan-400 font-bold mb-3">Column 1</h4>
            <p class="text-sm text-slate-300">Content</p>
        </div>
        <div class="bg-slate-800 p-6 rounded-xl border border-slate-700">
            <h4 class="text-emerald-400 font-bold mb-3">Column 2</h4>
            <p class="text-sm text-slate-300">Content</p>
        </div>
    </div>
</section>
```

Reuse across presentations by copying this section and customizing text/colors.

---

## Integration with Workflow

### Within VS Code

1. Activate `@presentHITs` in chat
2. Paste your content or attach a markdown file
3. Receive HTML presentation
4. Preview in browser (file → open with browser)
5. Export to PPTX if needed

### With Markdown Files

Provide markdown outline:
```markdown
# Title Slide

# Section 1
- Key point 1
- Key point 2

# Section 2 Metrics
- Metric A: 80%
- Metric B: 10k/day
```

@presentHITs will structure into proper slide deck with visual hierarchy.

---

## Next Steps

- **Customize colors** for your brand (update Tailwind classes)
- **Create template library** of repeating slide patterns
- **Integrate with CI/CD** to auto-generate status presentations
- **Build deck variations** (executive, technical, investor-focused) from same content

---

## Support

For issues or enhancements:
1. Check the **presentHITs.md** instruction file for core capabilities
2. Review **HTML Reference Template** for structure guidelines
3. Consult this guide for usage patterns
4. Test conversions with simple presentations first before complex ones
