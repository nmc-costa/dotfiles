#!/usr/bin/env node

/**
 * HTML-to-PPTX Converter for presentHITs
 * Converts interactive HTML slide presentations to PowerPoint format
 * 
 * Usage:
 *   node html-to-pptx-converter.js <input.html> [output.pptx]
 * 
 * Dependencies:
 *   npm install pptxgenjs
 * 
 * Example:
 *   node html-to-pptx-converter.js technophage_presentation.html technophage.pptx
 */

const fs = require('fs');
const path = require('path');
const PptxGenJs = require('pptxgenjs');

// Parse command-line arguments
const args = process.argv.slice(2);
if (args.length === 0) {
    console.error('❌ Usage: node html-to-pptx-converter.js <input.html> [output.pptx]');
    process.exit(1);
}

const inputFile = args[0];
const outputFile = args[1] || inputFile.replace('.html', '.pptx');

// Validate input file
if (!fs.existsSync(inputFile)) {
    console.error(`❌ Input file not found: ${inputFile}`);
    process.exit(1);
}

try {
    console.log(`📖 Reading HTML file: ${inputFile}`);
    const htmlContent = fs.readFileSync(inputFile, 'utf-8');
    
    // Parse slides from HTML
    const slides = parseHtmlSlides(htmlContent);
    
    if (slides.length === 0) {
        console.error('❌ No slides found in HTML file');
        process.exit(1);
    }
    
    console.log(`✓ Found ${slides.length} slides`);
    
    // Create PowerPoint presentation
    console.log('🎨 Creating PowerPoint presentation...');
    const prs = new PptxGenJs();
    
    // Set presentation properties
    prs.defineLayout({ name: 'LAYOUT1', width: 10, height: 7.5 });
    prs.defineLayout({ name: 'LAYOUT2', width: 10, height: 7.5 });
    prs.defineLayout({ name: 'LAYOUT3', width: 10, height: 7.5 });
    
    // Add slides to presentation
    slides.forEach((slide, index) => {
        addSlideToPresentation(prs, slide, index);
    });
    
    // Save presentation
    console.log(`💾 Saving to: ${outputFile}`);
    prs.writeFile({ fileName: outputFile });
    
    console.log(`✅ Presentation created successfully!`);
    console.log(`📊 Output: ${path.resolve(outputFile)}`);
    
} catch (error) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
}

/**
 * Parse HTML slides from content
 */
function parseHtmlSlides(htmlContent) {
    const slides = [];
    
    // Extract all <section class="slide"> or <div class="slide"> elements
    const sectionRegex = /<(?:section|div)[^>]*class="[^"]*slide[^"]*"[^>]*>([\s\S]*?)<\/(?:section|div)>/gi;
    let match;
    
    while ((match = sectionRegex.exec(htmlContent)) !== null) {
        const sectionContent = match[1];
        const slide = parseSlideContent(sectionContent);
        slides.push(slide);
    }
    
    return slides;
}

/**
 * Parse individual slide content with enhanced structure
 */
function parseSlideContent(sectionContent) {
    const slide = {
        title: '',
        subtitle: '',
        content: [],
        layout: 'title-and-content',
        elements: [], // Raw elements for better layout control
        isTitleSlide: false
    };
    
    // Extract title (h1, h2, h3, h4)
    const titleMatch = sectionContent.match(/<h[1-4][^>]*>([\s\S]*?)<\/h[1-4]>/i);
    if (titleMatch) {
        slide.title = cleanHtml(titleMatch[1]);
    }
    
    // Check if it's a title slide (h1 with text-6xl)
    if (sectionContent.includes('text-6xl') || sectionContent.includes('text-7xl')) {
        slide.isTitleSlide = true;
    }
    
    // Extract subtitle (p with text-xl, text-2xl, or text-lg)
    const subtitleMatch = sectionContent.match(/<p[^>]*class="[^"]*text-(?:xl|2xl|lg)[^"]*"[^>]*>([\s\S]*?)<\/p>/i);
    if (subtitleMatch) {
        slide.subtitle = cleanHtml(subtitleMatch[1]);
    }
    
    // Extract structured content blocks with color information
    const blockRegex = /<div[^>]*class="([^"]*)"[^>]*>([\s\S]*?)<\/div>/gi;
    let blockMatch;
    let blockCount = 0;
    
    while ((blockMatch = blockRegex.exec(sectionContent)) !== null) {
        const classes = blockMatch[1];
        const blockContent = blockMatch[2];
        
        // Skip if it's navigation or progress bar
        if (classes.includes('nav-controls') || classes.includes('progress-bar')) continue;
        
        // Determine block type and color
        let blockType = 'default';
        let blockColor = 'slate';
        
        if (classes.includes('bg-emerald-900') || classes.includes('bg-emerald-950')) {
            blockColor = 'emerald';
        } else if (classes.includes('bg-indigo-900') || classes.includes('bg-indigo-950')) {
            blockColor = 'indigo';
        } else if (classes.includes('bg-cyan-900')) {
            blockColor = 'cyan';
        } else if (classes.includes('bg-sky-900')) {
            blockColor = 'sky';
        } else if (classes.includes('bg-slate-800') || classes.includes('bg-slate-900')) {
            blockColor = 'slate';
        }
        
        if (classes.includes('grid') && classes.includes('grid-cols')) {
            blockType = 'grid';
        } else if (classes.includes('stage-card') || classes.includes('stage-cell')) {
            blockType = 'stage-card';
        }
        
        const cleanContent = extractStructuredContent(blockContent);
        if (cleanContent && blockCount < 5) {
            slide.elements.push({
                type: blockType,
                color: blockColor,
                content: cleanContent
            });
            blockCount++;
        }
    }
    
    // Extract list items with better structure
    const listRegex = /<li[^>]*>([\s\S]*?)<\/li>/gi;
    let listMatch;
    let listItems = [];
    
    while ((listMatch = listRegex.exec(sectionContent)) !== null) {
        const listItem = cleanHtml(listMatch[1]);
        if (listItem.trim()) {
            listItems.push(listItem);
        }
    }
    
    if (listItems.length > 0) {
        slide.content.push({
            type: 'list',
            items: listItems
        });
    }
    
    // Extract paragraphs as fallback
    const pRegex = /<p[^>]*>([\s\S]*?)<\/p>/gi;
    let pMatch;
    
    while ((pMatch = pRegex.exec(sectionContent)) !== null) {
        const pContent = cleanHtml(pMatch[1]);
        if (pContent.trim() && pContent !== slide.subtitle && pContent !== slide.title && pContent.length < 200) {
            slide.content.push({
                type: 'paragraph',
                text: pContent
            });
        }
    }
    
    return slide;
}

/**
 * Extract structured content from HTML blocks
 */
function extractStructuredContent(html) {
    const headings = [];
    const items = [];
    
    // Extract headings
    const headRegex = /<h[3-6][^>]*>([\s\S]*?)<\/h[3-6]>/gi;
    let headMatch;
    while ((headMatch = headRegex.exec(html)) !== null) {
        headings.push(cleanHtml(headMatch[1]));
    }
    
    // Extract list items
    const liRegex = /<li[^>]*>([\s\S]*?)<\/li>/gi;
    let liMatch;
    while ((liMatch = liRegex.exec(html)) !== null) {
        items.push(cleanHtml(liMatch[1]));
    }
    
    // Extract paragraphs
    const pRegex = /<p[^>]*class="[^"]*(?!nav|progress)[^"]*"[^>]*>([\s\S]*?)<\/p>/gi;
    let pMatch;
    while ((pMatch = pRegex.exec(html)) !== null) {
        const text = cleanHtml(pMatch[1]);
        if (text.trim()) items.push(text);
    }
    
    return {
        headings: headings,
        items: items.slice(0, 6) // Limit to 6 items per block
    };
}

/**
 * Clean HTML tags and entities
 */
function cleanHtml(html) {
    return html
        .replace(/<[^>]*>/g, '')  // Remove all HTML tags
        .replace(/&nbsp;/g, ' ')  // Replace non-breaking spaces
        .replace(/&quot;/g, '"')  // Replace quotes
        .replace(/&amp;/g, '&')   // Replace ampersands
        .replace(/&lt;/g, '<')    // Replace less-than
        .replace(/&gt;/g, '>')    // Replace greater-than
        .replace(/\s+/g, ' ')     // Collapse multiple spaces
        .trim();
}

/**
 * Add slide to PowerPoint presentation with enhanced styling
 */
function addSlideToPresentation(prs, slide, index) {
    const slide_layout = prs.addSlide();
    
    // Set slide background - dark theme
    slide_layout.background = { color: '0F172A' }; // Slate-900
    
    // Color mapping from Tailwind to PowerPoint RGB
    const colorMap = {
        'sky': '0EA5E9',      // sky-400
        'cyan': '06B6D4',     // cyan-400
        'emerald': '10B981',  // emerald-500
        'indigo': '6366F1',   // indigo-500
        'slate': 'E2E8F0'     // slate-100
    };
    
    if (slide.isTitleSlide) {
        // Title slide layout
        const titleSize = 54;
        slide_layout.addText(slide.title, {
            x: 0.5,
            y: 2.5,
            w: 9,
            h: 1.5,
            fontSize: titleSize,
            bold: true,
            color: '38BDF8', // Gradient approximation - cyan
            fontFace: 'Segoe UI',
            align: 'center'
        });
        
        // Separator line
        slide_layout.addShape('rect', {
            x: 3.5,
            y: 4.1,
            w: 3,
            h: 0.08,
            fill: { color: '06B6D4' },
            line: { color: '06B6D4', width: 0 }
        });
        
        // Subtitle
        if (slide.subtitle) {
            slide_layout.addText(slide.subtitle, {
                x: 0.5,
                y: 4.4,
                w: 9,
                h: 1.5,
                fontSize: 20,
                color: 'A8D5E2', // Lighter cyan
                fontFace: 'Segoe UI',
                align: 'center',
                italic: true
            });
        }
        
        return;
    }
    
    // Content slide layout
    let yOffset = 0.5;
    
    // Add title with underline
    if (slide.title) {
        slide_layout.addText(slide.title, {
            x: 0.5,
            y: yOffset,
            w: 9,
            h: 0.8,
            fontSize: 40,
            bold: true,
            color: '0EA5E9', // Sky-400
            fontFace: 'Segoe UI'
        });
        
        // Title underline
        slide_layout.addShape('rect', {
            x: 0.5,
            y: yOffset + 0.85,
            w: 2,
            h: 0.06,
            fill: { color: '0EA5E9' },
            line: { color: '0EA5E9', width: 0 }
        });
        
        yOffset += 1.3;
    }
    
    // Add subtitle if present
    if (slide.subtitle && slide.subtitle.length > 0) {
        slide_layout.addText(slide.subtitle, {
            x: 0.5,
            y: yOffset,
            w: 9,
            h: 0.5,
            fontSize: 16,
            color: 'CBD5E1', // Slate-300
            fontFace: 'Segoe UI',
            italic: true
        });
        yOffset += 0.7;
    }
    
    // Add structured elements from HTML
    if (slide.elements && slide.elements.length > 0) {
        const elementsPerRow = slide.elements.length > 2 ? 3 : 2;
        const elementWidth = (9 - 0.5) / elementsPerRow;
        const elementHeight = 1.8;
        
        let elementIndex = 0;
        for (let i = 0; i < slide.elements.length; i++) {
            const element = slide.elements[i];
            const row = Math.floor(i / elementsPerRow);
            const col = i % elementsPerRow;
            
            const xPos = 0.5 + (col * (elementWidth + 0.2));
            const yPos = yOffset + (row * (elementHeight + 0.3));
            
            if (yPos + elementHeight > 6.8) break;
            
            // Add element background box
            const bgColor = colorMap[element.color] || 'CBD5E1';
            slide_layout.addShape('rect', {
                x: xPos,
                y: yPos,
                w: elementWidth,
                h: elementHeight,
                fill: { color: '1E293B', transparency: 20 }, // Slate-800 transparent
                line: { color: bgColor, width: 1 }
            });
            
            // Add element content
            let contentY = yPos + 0.1;
            
            if (element.content.headings && element.content.headings.length > 0) {
                slide_layout.addText(element.content.headings[0], {
                    x: xPos + 0.1,
                    y: contentY,
                    w: elementWidth - 0.2,
                    h: 0.35,
                    fontSize: 12,
                    bold: true,
                    color: bgColor,
                    fontFace: 'Segoe UI'
                });
                contentY += 0.4;
            }
            
            if (element.content.items && element.content.items.length > 0) {
                const itemsText = element.content.items.slice(0, 3).map(item => '• ' + item).join('\n');
                slide_layout.addText(itemsText, {
                    x: xPos + 0.1,
                    y: contentY,
                    w: elementWidth - 0.2,
                    h: elementHeight - contentY + yPos - 0.2,
                    fontSize: 9,
                    color: 'E2E8F0', // Slate-100
                    fontFace: 'Segoe UI',
                    wrap: true
                });
            }
        }
        
        yOffset += Math.ceil(slide.elements.length / elementsPerRow) * (1.8 + 0.3) + 0.3;
    }
    
    // Add content items (lists, paragraphs)
    if (slide.content && slide.content.length > 0) {
        slide.content.forEach((item, i) => {
            if (yOffset + 0.4 > 6.8) return;
            
            if (item.type === 'list') {
                const listText = item.items.map(li => '• ' + li).join('\n');
                slide_layout.addText(listText, {
                    x: 0.7,
                    y: yOffset,
                    w: 8.6,
                    h: 'auto',
                    fontSize: 12,
                    color: 'CBD5E1', // Slate-300
                    fontFace: 'Segoe UI',
                    wrap: true
                });
                yOffset += 0.35 * (item.items.length + 1);
            } else if (item.type === 'paragraph') {
                slide_layout.addText(item.text, {
                    x: 0.7,
                    y: yOffset,
                    w: 8.6,
                    h: 'auto',
                    fontSize: 12,
                    color: 'CBD5E1',
                    fontFace: 'Segoe UI',
                    wrap: true
                });
                yOffset += 0.5;
            }
        });
    }
    
    // Add slide number at bottom
    slide_layout.addText(`${index + 1} / 13`, {
        x: 9,
        y: 6.95,
        w: 0.8,
        h: 0.25,
        fontSize: 9,
        color: '64748B', // Slate-500
        align: 'right',
        fontFace: 'Segoe UI'
    });
}
