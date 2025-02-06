# Writing your docs

MkDocs is a static site generator that's specifically designed for creating project documentation. It uses Markdown to write and format your documentation, making it simple and straightforward. By default, your documentation source files will be stored in a directory named docs at the top level of your project, alongside your mkdocs.yml configuration file.

### **1. Root Directory**
At the root level of  project, you will have  `mkdocs.yml` configuration file and the `docs` directory.

```
my-project/
│
├── mkdocs.yml
└── docs/
    └── index.md
```

### **2. Home Page**
The `index.md` file in the `docs` directory will be your homepage. You can write your project's introduction and general information here.

### **3. Creating Multiple Pages**
You can create multiple Markdown files within the `docs` directory to generate different pages for your documentation. For example:

```
docs/
    └── index.md
    └── explanation.md
    └── How_To_Guide.md
    └── reference.md
    └── tutorial.md
```

### **4. Nested Directories**
To organize your content further, you can create subdirectories within the `docs` directory. Each subdirectory can contain additional Markdown files. For instance:

```
docs/
    └── index.md
    └── How_To_Guide/
        └── overview.md
        └── configuration-options.md
```

### **5. URLs for Generated Pages**
The layout of your files and directories will determine the URLs for your generated pages. For example:

- `docs/index.md` -> `/`
- `docs/How_To_Guide/overview.md` -> `/How_To_Guide/overview/`
- `docs/How_To_Guide/configuration-options.md` -> `/How_To_Guide/configuration-options/`

### **6. Navigation in `mkdocs.yml`**
You can define the navigation structure for your documentation site in the `mkdocs.yml` file. Here's an example:

```yaml
site_name: My Project Documentation
nav:
  - Home: index.md
  - Explanation: explanation.md
  - How To Guide:
      - Overview: How_To_Guide/overview.md
      - Configuration Options: How_To_Guide/configuration-options.md
  - Reference: reference.md
  - Tutorial: tutorial.md
```


